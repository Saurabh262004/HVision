from typing import List

class Banner:
  def __init__(self, title: str, standardItems: List[str], softPityStart: int = None, hardPity: int = None, rateUpItems: List[str] = []):
    self.title = title
    self.softPityStart = softPityStart
    self.hardPity = hardPity
    self.standardItems = standardItems
    self.rateUpItems = rateUpItems
