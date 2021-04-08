def text_to_score(text,wordmark_d):
    mark = 0
    head=text.split()[:-1]
    foot=text.split()[1:]
    for i in range(len(head)):
        head[i]=head[i]+" "+foot[i]
    for i in head:
       if(i.rstrip("!,?.’”") in wordmark_d.keys()):
        #    print(i.rstrip("!,?.’”"))
           mark += int(wordmark_d[i.rstrip("!,?.’”")])
           text=text.replace(i,'',1)
    for i in text.split():
       if(i.rstrip("!,?.’”") in wordmark_d.keys()):
        #    print(i.rstrip("!,?.’”"))
           mark += int(wordmark_d[i.rstrip("!,?.’”")])
    return mark

