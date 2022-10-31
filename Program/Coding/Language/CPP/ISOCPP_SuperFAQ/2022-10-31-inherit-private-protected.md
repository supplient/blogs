私有继承通常被用来访问protected member。
如果是composition（当做成员对象）的话，那就访问不了protected member了。（也不能override虚函数）
不过这也只是短期的解决方案，通常只是应急措施。
应当尽可能倾向于composition。

可以用`using`来改变某个（继承类可以访问的）基类函数的访问控制：
``` c++
class Base
{
protected:
    void f() {}
};

class Derived: public Base
{
public:
    using Base::f;
};
```