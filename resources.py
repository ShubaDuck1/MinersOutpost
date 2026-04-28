class Resource:
    valid_type = ['wood', 'stone', 'coal', 'iron'];
    
    def __init__(self):
        self.type = None;
        self.amount = 0;
        
    def add(self, type, amount = 1):
        if type not in self.valid_type:
            raise ValueError(f"Invalid type: {type}");
        
        if type != self.type:
            return False;
        
        self.amount += amount;
        return True;