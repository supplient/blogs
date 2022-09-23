https://isocpp.org/wiki/faq/basics-of-inheritance

基类的protect是用来给继承类提供接口保证的，不是用来提供数据访问的。
基类管理的数据应当放在基类的private中，而不是protect中。
否则当对基类内部数据结构作出修改时，继承类的代码就报废掉了。
因此,protect部分应为继承类提供稳定的接口。
* public：为外部类提供接口
* protected: 为继承类提供接口
* private：自己维护的数据

哲学：尽管我们总是希望能够提供一个稳定的接口给任何人，但现实是这通常会受限于时间而无法实现。
因此我们通常会牺牲protected部分的接口稳定性，把继承类也需要访问的数据直接放到protected部分。