class Resource:
    '''
    Lớp tài nguyên.
    
    Attributes:
        valid_type (list): danh sách các loại tài nguyên phù hợp.
        type (string): loại tài nguyên.
        amount (int): số tượng tài nguyên.
    '''
    
    valid_type = ['wood', 'stone', 'coal', 'iron'];
    
    def __init__(self, type = None, amount = 0):
        self.type = type;
        self.amount = amount;
        
    def add(self, type, amount = 1):
        '''
        Hàm thêm tài nguyên:
        
        Args:
            type (string): loại tài nguyên.
            amount (int): số lượng tài nguyên.
            
        Returns:
            bool: trả về True nếu thêm tài nguyên thành công, False nếu ngược lại.
        '''
        
        if type not in self.valid_type:
            raise ValueError(f"Invalid type: {type}");
        
        if not self.type:
            self.type = type;
        
        if type != self.type:
            return False;
        
        self.amount += amount;
        return True;
    
    def remove(self, type, amount = 1, reset_type = True):
        '''
        Hàm lấy đi tài nguyên.
        
        Attributes:
            type (string): loại tài nguyên.
            amount (int): số lượng tài nguyên.
            reset_type (bool, optional): khi lấy đi tài nguyên có đặt lại giá trị loại tài nguyên không.
            
        Returns:
            bool: trả về True nếu lấy đi tài nguyên thành công, False nếu ngược lại.
        '''
        
        if type != self.type:
            return False;
        
        if amount > self.amount:
            return False;
        
        self.amount -= amount;
        if reset_type and self.amount == 0:
            self.type = None;
        return True;