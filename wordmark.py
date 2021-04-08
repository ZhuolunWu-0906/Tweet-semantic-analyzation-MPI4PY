def text_to_score(text,wordmark_d):
    mark = 0
    head=text.split()[:-1]
    foot=text.split()[1:]
    for i in range(len(head)):
        head[i]=head[i]+" "+foot[i]
    for i in head:
       if(i.strip("!,?.‘’“”") in wordmark_d.keys()):
           mark += int(wordmark_d[i.strip("!,?.‘’“”")])
           text=text.replace(i,'',1)
    for i in text.split():
       if(i.strip("!,?.‘’“”") in wordmark_d.keys()):
           mark += int(wordmark_d[i.strip("!,?.‘’“”")])
    return mark

