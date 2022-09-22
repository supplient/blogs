https://isocpp.org/wiki/faq/assignment-operators

操作符重载的操作数中至少有一个是user defined class。

`operator []`总是只接受一个操作数：其他的操作符也都是这样，语言本身允许有多少操作数就只能重载为有多少操作数，语言本身规定的优先级也不可更改。

