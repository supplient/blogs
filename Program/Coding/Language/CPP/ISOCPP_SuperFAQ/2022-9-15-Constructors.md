[https://isocpp.org/wiki/faq/ctors](https://isocpp.org/wiki/faq/ctors)

constructor的常用缩写：ctor

`T x;`和`T x();`是不同的：
``` c++
void f()
{
    T x; // Declare a local object named x (of class T)
}

void g()
{
    T x(); // Declare a function named x (which returns a T object)
}
```

从C++11开始，可以在构造函数中调用同一个类的另一个构造函数：
``` c++
class X {
    int a;
public:
    X(int x) { if (0<x && x<=max) a=x; else throw bad_X(x); }
    X(string s):X{stoi(s)} {} // This will call another ctor: X(int)
};
```
注意必须要在构造函数列表里调用，不然就只是新建一个对象了而已。

不要在构造函数里直接操作this指针所指向的内存（例如，使用placement new：`new(this) T(args)`），因为对象内存在构造函数中是“部分构造”(partially constructed)的，而“部分构造”的对象是未定义的，不同实现下会得到不同的结果。
总之：**永远不要在构造函数里玩弄对象本身的内存**。

成员对象的初始化顺序与它们的声明顺序一致，而与构造函数的初始化列表里的初始化顺序无关，例如：
``` c++
class A
{
public:
    A() { cout << "A" << endl; }
};

class B
{
public:
    B() { cout << "B" << endl; }
};

class C
{
private:
    A a;
    B b;
public:
    C(): a(), b() {}
};

class D
{
private:
    B b;
    A a;
public:
    D(): a(), b() {}
};

int main()
{
    C c;
    // will print:
    // A
    // B
    D d;
    // will print:
    // B
    // A
    return 0;
}
```
不过通常还是建议要让初始化列表里的顺序和实际的初始化顺序保持一致：先基类（从左到右），再成员对象（从上到下）。
这只是为了方便调试，对实际的代码执行没有任何影响。

如上一条所述，初始化列表里的顺序 不决定 实际的初始化顺序，所以应尽量避免在初始化列表里对成员对象初始化顺序有依赖：
```c++
class C
{
private:
    int a;
    int b;
public:
    C(int x): a(x), b(a) {} // bad
};

class D
{
private:
    int a;
    int b;
public:
    D(int x): a(x), b(x) {} // good
};
```

但有时候就是会对成员对象的初始化顺序有要求，那么应用注释注明：
``` c++
class C
{
private:
    A a; // ORDER DEPENDENCY
    B b; // ORDER DEPENDENCY
public:
    C(): a(), b(a) {}
};
```

在基类构造函数里访问虚函数的时候访问不到继承类覆写的版本：
``` c++
#include <iostream>
using namespace std;


class A
{
public:
    A() { Func(); }

    virtual void Func() { cout << "A" << endl; }
};

class B: public A
{
public:
    B() { Func(); }

    virtual void Func() override { cout << "B" << endl; }
};


int main()
{
    B b;
    // B() ->
    // A() ->
    // A::Func() ->
    // B::Func()
    return 0;
}
```

