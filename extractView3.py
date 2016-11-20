基本方法： 将划分好的词与车名词典（爬取 + 官方提供的view）中的词进行最长子串匹配：
Ws
属于划分的词，Wc属于词典中词，以prevwords
记录当前待识别的车视角：

匹配过程：

理想的精确匹配（不完全可行）：
find_lcsubstr(Ws, Wc) == Ws.len == Wc.len

实际非精确匹配(划分3类)：
a、字母或数字或中文
if (find_lcsubstr(Ws, Wc) == Ws.len){
if (find_lcsubstr(prevwords + Ws, Wc) >= Ws.len + 2 / 3 * prevwords ){
prevwords += Ws;
}else{
if (checkandfix(prevwods)){
print(prevwords);
}
prevwords = Ws;
}

}
}else{
continue
}



b、中文
if (Ws.flag != "eng" or "m" & & find_lcsubstr(Ws, Wc) == 2 / 3 * Ws.len)
{
if (find_lcsubstr(prevwords + Ws, Wc)) > = 2 / 3 * Ws.len + 2 / 3 * prevwords {
prevwords += Ws;
}else{
if (check(prevwods)){
print(prevwords)
}
prevwords = Ws;
}

}

c、 " "
或
"-"
等特殊字符
if (prevwords != "")
{
prevwords += " " or "-"
} else{
continue;
}
