https://isocpp.org/wiki/faq/virtual-functions

``` c++
class A 
{
public:
    virtual void f() { cout << "A" << endl; }
};

class B: public A
{
public:
    virtual void f() { cout << "B" << endl; }
};

B b{};
b.A::f(); // OK, print "A"

B* pb = new B{};
pb->A::f(); // OK, print "A"
```

若基类函数为virtual，则继承类函数也自动为virtual，不管有没有显式声明：
``` c++
class A
{
public:
    virtual void f() {}
};

class B
{
public:
    void f() {} // auto virtual
};
```

Q：什么时候应该让析构函数是virtual的？
A：当继承类对象可能被用基类指针delete的时候。
这本质是因为继承类总是会重载基类的析构函数，基类和继承类的析构函数总是做不同的工作：基类的析构函数释放基类那部分对象；继承类的析构函数先释放继承类那部分对象，再调用基类的析构函数来释放基类那部分对象。
那如果同一个函数在继承类中被重载了，但它却不是虚函数的话，那通过基类指针调用该函数的时候就不会去调用继承类中的实现了。
这就导致继承类的析构函数没有被调用 -> 继承类的那部分对象没有被释放。

析构函数是特别的，它其实是所有类都有的一个“同名函数”：
``` c++
class A 
{
public:
    virtual ~A() { cout << "A" << endl; }
};

class B: public A
{
public:
    ~B() { cout << "B" << endl; }
};


int main()
{
    A* a = new B{};
    a->~A();
    cout << "end" << endl;

    // Output:
    // B
    // A
    // end

    return 0;
}
```
如上，当基类析构函数`~A`被显式调用时，继承类析构函数`~B`却被调用了。
我猜测原因是编译器看到`~A`时就直接把它翻译为对析构函数的调用了，而析构函数是virtual的，所以去查虚表了。
附带一提，如果显式调用`A::~A`的话，那就不会调用`~B`，而只会调用`~A`了。

Covariant Return Types：尽管不可以通过返回值来重载函数，但是却允许通过范围类型更小的返回值来覆盖函数。
``` c++
class A
{
public:
    virtual A* func() { /*...*/ }
};

class B
{
public:
    // This is OK
    B* func() { /*...*/ }
    // This is invalid
    int func() {}
};
```