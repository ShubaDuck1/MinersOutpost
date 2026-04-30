import queue;

class PlayerAction:
    def __init__(self, space):
        self.action_queue = queue.Queue();
        self.space = space;
        self.current_action = None;
    
    def add(self, destination):
        self.action_queue.put(destination);
        
    def update(self):
        cnt = self.space.count_not_busy();
        i = 0;
        
        while not self.action_queue.empty() and i < cnt:
            if not self.current_action:
                self.current_action = self.action_queue.get();
            tmp = self.space.find_path_miner(self.current_action);
            if tmp:
                dest_x, dest_y = self.current_action;
                curr_task = self.space.grid[dest_y][dest_x].structure;
                i += 1;
                miner, path = tmp;
                miner.set_path(path);
                miner.set_interact(curr_task);
        
                