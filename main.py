from dataclasses import dataclass
from PIL import Image
import numpy as np


Data = bytes


@dataclass
class ImageSteganography:
    
    depth: int = 2 # Number of bits per image byte to use for encoding the message.
    
    
    def encode(self, message: Data, size: int, image: Image) -> Image:
        
        image_bytes = np.array(image)
        orig_shape = image_bytes.shape
        image_bytes = image_bytes.flatten()
        
        i_message = 0
        i_image = 0
        
        while i_message < size - 1:
            
            message_byte = message[i_message]
            
            for j in range(8 // self.depth):
                
                image_byte = image_bytes[i_image]
                
                message_chunk = (message_byte >> self.depth*j) & ((1 << self.depth) - 1)
                new_image_byte = (image_byte & ~((1 << self.depth) - 1)) | message_chunk
               # print('{:08b}'.format(int(new_image_byte)), end=' ')
                
                image_bytes[i_image] = new_image_byte
                
                i_image += 1
            
            i_message += 1
            
        
        return Image.fromarray(image_bytes.reshape(orig_shape))
    
    
    def decode(self, image: Image, size: int) -> Data:
        
        image_bytes = np.array(image).flatten()
        message_bytes = list(bytes(size))
        i_image = 0
        i_message = 0
        
        while i_message < size - 1:
            
            message_byte = 0
            
            for j in range(8 // self.depth):
                
                image_byte = image_bytes[i_image]
                message_chunk = image_byte & ((1 << self.depth) - 1)
                
                print(message_chunk, end= ' ')
                
                message_byte |= message_chunk << (self.depth * j)
            
                i_image += 1
            
            message_bytes[i_message] = message_byte
            i_message += 1
        
        return message_bytes
   
