[https://isocpp.org/wiki/faq/dtors](https://isocpp.org/wiki/faq/dtors)

析构顺序与构造顺序总是相反的。

析构函数不可重载，它总是以`T::~T()`的形式出现，不接受任何参数。

* new: 分配内存 -> 调用构造函数
	* 有点像python里的`__new__` -> `__init__`
* delete: 调用析构函数 -> 回收内存
* placement new: 仅调用构造函数
* 局部变量/全局变量结束其生命周期时：调用析构函数 -> 回收内存
	* 注意：形如`T*`的指针变量在结束生命周期时并不会对其指向的对象调用析构，也不会回收其内存，只是这个指针变量本身的内存会被回收而已。

`operator new`本身也可以被重载（[参考资料](https://www.geeksforgeeks.org/overloading-new-delete-operator-c/)）：
``` c++
class T
{
public:
    T() 
    {
        cout << "Constructing..." << endl;
    }

    void* operator new(size_t size)
    {
        cout<< "Overloading new operator with size: " << size << endl;
        return ::operator new(size);
    }

	void* operator new(size_t size, char c)
	{
		cout << "Get char: " << c << endl;
		return T::operator new(size);
		// Note: if write
        // 		return new T();
		// the constructor will be called twice.
	}
 
    void operator delete(void * p)
    {
        cout<< "Overloading delete operator " << endl;
        free(p);
    }
};
 
int main()
{
    T* p = new T();
    delete p;
    cout << endl;

	p = new('c') T();
	delete p;
    cout << endl;
}

/* Output：
Overloading new operator with size: 1
Constructing...
Overloading delete operator 

Get char: c
Overloading new operator with size: 1
Constructing...
Overloading delete operator
*/
```
要注意的是`operator new`和`operator delete`负责的只是内存的分配/回收那一部分，并不是把整个`new, delete`都给重载了。
**也就是说，如果在operator new里调用了构造函数的话，那就会导致构造函数被调用两次。**

**不要在析构函数中抛出异常**。
* 规则1：在处理一个异常时如果又抛出了一个异常的话，那程序会被立即终止。
* 规则2：处理一个异常的过程总是从它被`throw`的地方一直stack unwinding到它被`catch`的地方。
	* stack unwinding：弹出途径的所有栈帧，并对栈帧中的所有局部变量调用其析构函数。
* 综合规则1和2，如果在处理一个异常时，stack unwinding的过程中有某个局部变量的析构函数又抛出了异常的话，那程序会被立即终止。