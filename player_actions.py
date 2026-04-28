import queue;

class PlayerAction:
    def __init__(self):
        self.action_queue = queue.Queue();
    
    def add(self, destination):
        self.action_queue.put(destination);
        
    def update(self, space):
        cnt = space.count_not_busy();
        
        for i in range(cnt):
            while not (self.action_queue.empty() 
                       or space.find_path_miner(self.action_queue.get())):
                pass;