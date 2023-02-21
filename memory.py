import tiktoken

class Memory:
  def __init__(self, separator="\n\n", max_tokens=1000):
    self.separator = separator
    self.max_tokens = max_tokens

    self.queue = []
    self.total_tokens = 0
    self.encoding = tiktoken.get_encoding("gpt2")
  
  def size(self):
    return len(self.queue)
    
  def push(self, string):
    tokens = self.__count_tokens(
      "{string}{separator}".format(string=string, separator=self.separator)
    )

    self.queue.append({
      "string": string,
      "tokens": tokens
    })

    self.total_tokens += tokens

    while (len(self.queue) > 0 and self.total_tokens > self.max_tokens):
      first_entry = self.queue.pop(0)
      self.total_tokens -= first_entry["tokens"]
  
  def serialize(self):
    if len(self.queue) == 0:
      return ""

    return self.separator.join(
      map(lambda x: x["string"], self.queue)
    )
      
  def __count_tokens(self, string):
    return len(self.encoding.encode(string))
