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

static const成员变量也需要被显式定义，并且必须被初始化赋值。
``` c++
// 非法：没有初始化赋值
class T {
public:
    static const int x;
};
const int Fred::x;

// 非法：没有显式定义
class Fred {
public:
    static const int x = 3;
};
```
初始化赋值时可以在声明处初始化，也可以在定义处初始化。
* 声明处初始化时，该成员变量会被优化为编译期常量（不过依然可以对它取地址），所以初始化表达式也必须是编译期可求值的。
* 定义处初始化时没有任何限制。
``` c++
// 合法：声明处初始化
class T
{
public:
    static const int x=3;
};
const int T::x;

// 非法：声明处初始化表达式编译期不可求值
int y=4;
class T
{
public:
    static const int x=y;
};
const int T::x;

// 合法：定义处初始化
int y=4;
class T
{
public:
    static const int x;
};
const int T::x=y;

// 非法：重复初始化
class T
{
public:
    static const int x=3;
};
const int T::x=4;
```

static变量的构造顺序和析构顺序都是不可控的，应尽可能避免在static变量的构造过程、析构过程（包括构造函数和初始化表达式）中依赖其他static变量。

若一个对象的构造函数抛出异常，则为这个对象分配的内存会被自动回收，所以并不会发生内存泄漏。

Named Parameter Idiom：就是让成员函数返回自己的引用，于是就能一直.下去了，一般好像也不叫它Named Parameter Idiom……
iostream那套就是这么实现的。
``` c++
class File;
class OpenFile {
public:
  OpenFile(const std::string& filename);
    // sets all the default values for each data member
  OpenFile& readonly();  // changes readonly_ to true
  OpenFile& readwrite(); // changes readonly_ to false
  OpenFile& createIfNotExist();
  OpenFile& blockSize(unsigned nbytes);
  // ...
private:
  friend class File;
  std::string filename_;
  bool readonly_;          // defaults to false [for example]
  bool createIfNotExist_;  // defaults to false [for example]
  // ...
  unsigned blockSize_;     // defaults to 4096 [for example]
  // ...
};

File f = OpenFile("foo.txt")
           .readonly()
           .createIfNotExist()
           .appendWhenWriting()
           .blockSize(1024)
           .unbuffered()
           .exclusiveAccess();

// File.cpp
File::File(const OpenFile& params)
{
  // ...
}
```

```c++
class B {
public:
    B() {}
};
class A {
public:
    A(B) {
        //...
    }
};

A a(B());
a.func(); // Failed
```
上文中`A a(B())`会报错，这是因为编译器先读到`A a(...)`，它会以为这是一句函数声明，以为这是一个叫`a`的函数：
这个函数返回一个`A`对象，其参数也是一个函数。
`B()`被认为是一个函数类型，它描述的是返回一个`B`对象的、参数列表为空的函数（用`B(*)()`的写法或许会更熟悉）。
也就是说上文中`a`的类型被编译期认定为`A(*)(B(*)())`，而不是我们以为的`A`。
为了解决这一问题，最好的方法是使用uniform initialization：
``` c++
A a{B()};
a.func(); // Work
```

`explicit`关键字可以用来避免构造函数被用来进行隐式类型转换。









