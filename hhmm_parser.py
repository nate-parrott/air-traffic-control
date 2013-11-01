from __future__ import division

MAX_CANDIDATE_DEPTH = 10

def tokenize(string):
    return string.lower().split(' ')

def is_production_state(state):
    return state[0]==state[0].lower()

def preprocess_sample(sample):
    # automatically wraps text in secondary tags with production tags:
    tag = sample[0]
    items = sample[1:]
    tag_is_production = tag[0]==tag[0].lower()
    i = 0
    new_items = []
    for item in items:
        if type(item)==str:
            if not is_production_state(tag):
                # wrap it:
                synthetic_tag_name = tag.lower()
                tags_before = [prev_item[0] for prev_item in items[:i] if type(prev_item)==list]
                tags_after = [post_item[0] for post_item in items[i+1:] if type(post_item)==list]
                if len(tags_after): synthetic_tag_name += '-pre-'+tags_after[0]
                elif len(tags_before): synthetic_tag_name += '-post-'+tags_before[-1]
                new_items.append([synthetic_tag_name, item])
            else:
                new_items.append(item)
        else:
            new_items.append(preprocess_sample(item))
        i += 1
    return [tag]+new_items

from collections import defaultdict

class ProbabilityCounter(object):
    def __init__(self):
        self.counts = defaultdict(int)
    def sample(self, event):
        self.counts[event] += 1
    def __getitem__(self, event):
        return (self.counts[event] if event in self.counts else 0)/sum(self.counts.values())
    def iterprobs(self):
        return ((event, self[event]) for event in self.counts.iterkeys())

class MarkovContext(object):
    def __init__(self):
        self.state_transition_probabilities = defaultdict(ProbabilityCounter)

class Candidate(object):
    def __init__(self, parser):
        self.context_stack = []
        self.state_stack = []
        self.prob = 1.0
        self.parser = parser
        self.stack_snapshots = []
    def copy(self):
        c = Candidate(self.parser)
        c.context_stack = self.context_stack[:]
        c.state_stack = self.state_stack[:]
        c.prob = self.prob
        c.stack_snapshots = self.stack_snapshots[:]
        return c
    def state_id(self):
        return tuple(self.state_stack)
    def candidates_by_transitioning_to_next_state(self, max_recurs=6):
        if max_recurs==0: return []
        ctx = self.context_stack[-1]
        cur_state = self.state_stack[-1]
        children = []
        for next_state, prob in ctx.state_transition_probabilities[cur_state].iterprobs():
            child = self.copy()
            child.state_stack[-1] = next_state
            child.prob *= prob*(1-self.parser.smoothing) + self.parser.smoothing
            if next_state=='$end':
                if len(child.context_stack)>1:
                    child.context_stack.pop()
                    child.state_stack.pop()
                    children += child.candidates_by_transitioning_to_next_state(max_recurs-1)
                #else:
                #    children.append(child)
            elif is_production_state(next_state):
                children.append(child)
            else:
                deeper_ctx = self.parser.markov_contexts[next_state]
                child.context_stack.append(deeper_ctx)
                child.state_stack.append('$start')
                children += child.candidates_by_transitioning_to_next_state(max_recurs-1)
        return children
    def prob_of_ending(self):
        p = 1
        for i in xrange(len(self.context_stack)):
            ctx = self.context_stack[i]
            state = self.state_stack[i]
            p *= ctx.state_transition_probabilities[state]['$end']*(1-self.parser.smoothing) + self.parser.smoothing
        return p
    def structure(self):
        struct = []
        struct_stack = [struct]
        for i in xrange(len(self.stack_snapshots)):
            snapshot = self.stack_snapshots[i]
            prev_snapshot = [] if i==0 else self.stack_snapshots[i-1]
            same_until = 0
            while same_until<len(snapshot) and same_until<len(prev_snapshot) and snapshot[same_until]==prev_snapshot[same_until]:
                same_until+=1
            for removed in prev_snapshot[same_until:]:
                struct_stack.pop()
            for added in snapshot[same_until:]:
                new_struct = [added]
                struct_stack[-1].append(new_struct)
                struct_stack.append(new_struct)
            struct_stack[-1].append(self.parser.tokens[i])
        return struct

class Parser(object):
    def __init__(self, samples):
        self.markov_contexts = {}
        self.emission_probs = {} #self.emission_probs[state][n-gram]
        self.process_samples(samples)
        self.smoothing = 0.1
    def process_samples(self, samples):
        for sample in samples:
            sample = ["Result", sample]
            sample = preprocess_sample(sample)
            self.process_sample(sample)
    def process_sample(self, sample):
        state = sample[0]
        if state in self.markov_contexts:
            ctx = self.markov_contexts[state]
        else:
            ctx = MarkovContext()
            self.markov_contexts[state] = ctx
        prev_child_state = '$start'
        for child in sample[1:]:
            child_state = child[0]
            ctx.state_transition_probabilities[prev_child_state].sample(child_state)
            prev_child_state = child_state
            if is_production_state(child_state):
                if child_state not in self.emission_probs:
                    self.emission_probs[child_state] = ProbabilityCounter()
                for token in tokenize(child[1]):
                    ngram = (token,)
                    self.emission_probs[child_state].sample(ngram)
                for self_transition in xrange(0, len(tokenize(child[1]))-1):
                    ctx.state_transition_probabilities[child_state].sample(child_state)
            else:
                self.process_sample(child)
        ctx.state_transition_probabilities[prev_child_state].sample('$end')
    def parse(self, tokens):
        self.tokens = tokens
        origin = Candidate(self)
        origin.context_stack = [self.markov_contexts['Result']]
        origin.state_stack = ['$start']
        candidates = origin.candidates_by_transitioning_to_next_state()
        for i in xrange(len(tokens)):
            #print '\n\n'
            #print tokens[i]
            new_cands = {}
            for cand in candidates:
                #print cand.state_stack, cand.prob
                for child in cand.candidates_by_transitioning_to_next_state():
                    for n in (1,):#xrange(1, min(2, i+1)):
                        ngram = tuple(tokens[i+1-n:i+1])
                        emission_prob = self.emission_probs[child.state_stack[-1]][ngram]
                        child.prob *= emission_prob*(1-self.smoothing) + self.smoothing
                    id = child.state_id()
                    if len(child.state_stack)<=MAX_CANDIDATE_DEPTH and (id not in new_cands or new_cands[id].prob < child.prob):
                        new_cands[id] = child
            candidates = new_cands.values()
            for c in candidates:
                c.stack_snapshots.append(c.state_stack[:])
            i += 1
        for cand in candidates:
            cand.prob *= cand.prob_of_ending()
        candidates.sort(key=lambda c: c.prob, reverse=True)
        return candidates

if __name__=='__main__':
    samples = [
		["Dispatch", ["Plane", "Emirates 209"], "please", ["Command", ["Taxi", "taxi to", ["Place", "runway 2"]]]],
		["Dispatch", ["Plane", "Swissair 11"], "you're cleared for", ["Command", ["Takeoff", "takeoff"]]],
		["Dispatch", ["Plane", "American 42"], ["Command", ["Taxi", "go to", ["Place", "gate C13"]]]],
		["Dispatch", ["Plane", "United 78"], "please", ["Command", ["Ascend", "climb to", ["Altitude", "30,000 feet"]]]],
		["Dispatch", ["Plane", "Delta 92"], ["Query", ["AltitudeQuery", "what's your altitude ?"]]],
		["Dispatch", ["Plane", "American 32"], "you're cleared for", ["Command", ["Landing", "landing on", ["Place", "runway 1"]]]]
    ]
    p = Parser(samples)
    cands = p.parse(tokenize("Emirates 33 please climb to 50,000 feet"))
    print cands[0].structure()
