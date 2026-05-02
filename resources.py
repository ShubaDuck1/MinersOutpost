class Resource:
    valid_type = ['wood', 'stone', 'coal', 'iron'];
    
    def __init__(self, type = None, amount = 0):
        self.type = type;
        self.amount = amount;
        
    def add(self, type, amount = 1):
        if type not in self.valid_type:
            raise ValueError(f"Invalid type: {type}");
        
        if not self.type:
            self.type = type;
        
        if type != self.type:
            return False;
        
        self.amount += amount;
        return True;
    
    def remove(self, type, amount = 1):
        if type != self.type:
            return False;
        
        if amount > self.amount:
            return False;
        
        self.amount -= amount;
        if self.amount == 0:
            self.type = None;
        return True;