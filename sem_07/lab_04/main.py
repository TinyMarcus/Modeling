import numpy.random as nr

class GeneratorRandom:
    def __init__(self, a, b, mu, sigma):
        self.a = a
        self.b = b
        self.mu = mu
        self.sigma = sigma

    def ed_random(self):
        return nr.uniform(self.a, self.b)
    
    def norm_random(self):
        return nr.normal(self.mu, self.sigma)

class GenerateRequest:
    def __init__(self, generator, count):
        self.generator = generator
        self.cnt_requests = count

    def generate_request(self):
        self.cnt_requests = self.cnt_requests - 1
    
    def delay(self):
        time = -1
        while time < 0:
            time = self.generator.ed_random()
        return time

class ProcessRequest:
    def __init__(self, generator, p):
        self.generator = generator
        self.queue = 0
        self.received = 0
        self.max_queue = 0
        self.reenters = 0
        self.processed = 0
        self.p = p
    
    def receive_request(self):
        self.queue = self.queue + 1
        self.received = self.received + 1
        self.max_queue = max(self.max_queue, self.queue)

    def delay(self):
        time = -1
        while time < 0:
            time = self.generator.norm_random()
        return time
    
    def process(self):
        if self.queue > 0:
            self.queue = self.queue - 1
            self.processed = self.processed + 1
        if nr.random_sample() < self.p:
            self.reenters = self.reenters + 1
            self.receive_request()
        
class Modeling:
    def __init__(self, generator, processor):
        self.generator = generator
        self.processor = processor
    
    def event_principle(self):
        generated_time = self.generator.delay()
        processed_time = generated_time + self.processor.delay()
        cnt_requests = self.generator.cnt_requests

        while self.processor.processed < cnt_requests + self.processor.reenters:
            if generated_time <= processed_time:
                self.generator.generate_request()
                self.processor.receive_request()
                generated_time = generated_time + self.generator.delay()
            else:
                self.processor.process()
                if self.processor.queue > 0:
                    processed_time = processed_time + self.processor.delay()
                else:
                    processed_time = generated_time + self.processor.delay()

        result = {"Processed requests": self.processor.processed,
                  "Reenters requests": self.processor.reenters,
                  "Max queue": self.processor.max_queue,
                  "Processed time": processed_time}

        return result

    def dt_principle(self, dt):
        generated_time = self.generator.delay()
        processed_time = generated_time + self.processor.delay()
        cnt_requests = self.generator.cnt_requests
        current_time = 0

        while self.processor.processed < cnt_requests + self.processor.reenters:
            if generated_time <= processed_time:
                self.generator.generate_request()
                self.processor.receive_request()
                generated_time = generated_time + self.generator.delay()
            if processed_time < current_time:
                self.processor.process()
                
                if self.processor.queue > 0:
                    processed_time = processed_time + self.processor.delay()
                else:
                    processed_time = generated_time + self.processor.delay()
            
            current_time = current_time + dt

        result = {"Processed requests": self.processor.processed,
                  "Reenters requests": self.processor.reenters,
                  "Max queue": self.processor.max_queue,
                  "Processed time": current_time}

        return result

if __name__ == "__main__":
    a = 1
    b = 8
    mu = 0
    sigma = 3
    n = 1000
    p = 0.99
    dt = 1

    random_generator = GeneratorRandom(a, b, mu, sigma)
    generator = GenerateRequest(random_generator, n)
    processor = ProcessRequest(random_generator, p)
    model = Modeling(generator, processor)
    result = model.event_principle()

    print("==============================================")
    print("Event principle\n")
    print("Count of processed requests: {}".format(result['Processed requests']))
    print("Count of re-processed requests: {}".format(result['Reenters requests']))
    print("Length of queue: {}".format(result['Max queue']))
    print("Time of processing: {}".format(result['Processed time']))

    random_generator = GeneratorRandom(a, b, mu, sigma)
    generator = GenerateRequest(random_generator, n)
    processor = ProcessRequest(random_generator, p)
    model = Modeling(generator, processor)
    result = model.dt_principle(dt)

    print("\n\n==============================================")
    print("ΔT principle\n")
    print("Count of processed requests: {}".format(result['Processed requests']))
    print("Count of re-processed requests: {}".format(result['Reenters requests']))
    print("Length of queue: {}".format(result['Max queue']))
    print("Time of processing: {}".format(result['Processed time']))
