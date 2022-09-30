https://isocpp.org/wiki/faq/strange-inheritance#protected-virtuals

* public virtual是对外的接口，向使用这套类的代码提供统一的约定。
* protected virtual是对内的接口，向这套类的内部实现提供统一的约定。

#### Protected Virtuals
*Public Overloaded Non-Vrituals Call Protected Non-Overloaded Viftuals* idiom:
``` c++
class Base {
public:
  void f(int x)    { f_int(x); }  // Non-virtual
  void f(double x) { f_dbl(x); }  // Non-virtual
protected:
  virtual void f_int(int);
  virtual void f_dbl(double);
};
```
如果这套类（基类+继承类）对外的接口都一模一样，只是实现不同而已的话，
那可以把所有接口都放在基类里，做成non-virtual的，
从而确保所有继承类都不需要关心对外接口的设计问题。
继承类只需要关注内部的virtual protected方法实现即可。


#### Private Virtuals
*Template Method* pattern:
``` c++
class MyBaseClass {
public:
  void myOp();
private:
  virtual void myOp_step1() = 0;
  virtual void myOp_step2();
};
void MyBaseClass::myOp()
{
  // Pre-processing...
  myOp_step1();  // call into the future - call the derived class
  myOp_step2();  // optionally the future - this one isn't pure virtual
  // Post-processing...
}
void MyBaseClass::myOp_step2()
{
  // this is "default" code - it can optionally be customized by a derived class
}
```
private virtual和protected virtual其实差不多，它们都是对内的接口。
不过private virtual的话范围更小，是只对“基类”的接口。
通常来说我们更倾向于protected virtual，因为设计基类的时候很难确定继承类是否会调用这些接口。

构造函数内不可调用virtual methods.