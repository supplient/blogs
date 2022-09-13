https://isocpp.org/wiki/faq/classes-and-objects

stuct与class是等价的，但大家通常还是习惯把struct用作弱封装，而把class用作强封装。

C里的static变量在C++里被废弃了。（指的是将作用域限定在当前文件的static变量，不是指函数体内的静态生命周期static变量）

const类变量和非const类变量一样，也需要out-of-class的定义后才能被作为右值使用：
```C++
class AE {
    // ...
    public:
    static const int c6 = 7;
    static const int c7 = 31;
};

const int AE::c7; // definition

void byref(const int&);

int f()
{
    byref(AE::c6); // error: c6 not an lvalue
    byref(AE::c7); // ok
    const int* p1 = &AE::c6; // error: c6 not an lvalue
    const int* p2 = &AE::c7; // ok
    // ...
}
```

对象的内存排布(memory layout)：没有严格规定，大抵上就是一个成员变量接着另一个成员变量。然后如果有虚函数的话就给对象再加一个指向虚表的指针，然后虚表是在这个类的所有对象之间共享的。

空类的对象的大小也一定不是0：这是为了确保任何对象都具有独一无二的地址。
不过有个叫"empty base class optimization"的东西算是半个特例：一个空类的对象的大小不为0，但在它的子类的对象中并没有空类对象的大小，从而避免了浪费内存。例：
```c++
struct X : Empty {
    int a;
    // ...
};

void f(X* p)
{
    void* p1 = p;
    void* p2 = &p->a;
    if (p1 == p2) cout << "nice: good optimizer";
}
```
这一优化在C++11之后就是强制要求了，不再是编译器特性。