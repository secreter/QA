arr=['wqwq','wqw/wqwq']
print([item  if len(item.split('/'))>1 else '/'+item for item in arr])
Do-something if <condition>, else do-something else.