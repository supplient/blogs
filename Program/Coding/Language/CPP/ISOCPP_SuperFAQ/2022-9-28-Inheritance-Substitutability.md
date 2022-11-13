https://isocpp.org/wiki/faq/proper-inheritance

`Derived** -> Base**`的转换是危险的，它会导致继承类B的指针能指向另一个继承类C的对象。
``` c++
class A
{
public:
    virtual void func() { cout << "A" << endl; }
};

class B: public A
{
public:
    void func() { cout << "B" << endl; }
};

class C: public A
{
public:
    void func() { cout << "C" << endl; }
};
 
int main()
{
    B b;
    B* bp = &b; // bp => b
    B** bpp = &bp; // bpp => bp => b

    // !!! THIS MATTERS !!!
    A** app = (A**)bpp; // app => bp => b

    C c;
    C* cp = &c; // cp => c
    // `*app` is the ref for `bp`(i.e. B*&), so modify `*app` will change the value of `bp`,
    //     meaning the address of `b` saved in `bp` will be replaced by 
    //     the address of `c` which is saved in `cp`.
    *app = cp; // app => bp => c

    bp->func(); // C

    return 0;
}
```
根本问题在于如果我们能用`Base** basePtrPtr`去指向一个继承类的指针`Derived_A* daPtr`的话：
``` c++
basePtrPtr = (Base**)&daPtr;
```
那么同样的基类指针的指针当然也能指向另一个继承类的指针`Derived_B* dbPtr`。
而因为对基类指针的指针进行解引用时得到的其实是对继承类指针的引用：
``` c++
(*basePtrPtr) === daPtr
type(*basePtrPtr) === Derived_A*&
```
所以对基类指针的指针的解引用进行修改时修改的其实是继承类的指针：
``` c++
*basePtrPtr = dbPtr; // Actually, `daPtr` is modified.
```
结果就导致`daPtr`里的地址被替换为`dbPtr`里的地址，也就是说`daPtr`指向了一个`Derived_B`对象。


继承类对象的容器不应转换为基类对象的容器，那是极其危险的。
不过继承类对象的指针的容器可以安全地转换为基类对象的指针的容器。
两者的根本区别在于容器类的方法需不需要重载（对象容器需要，指针容器不需要）。
考虑用数组做容器类：
``` c++
class A
{
public:
    virtual void func() { cout << "A" << endl; }
};

class B: public A
{
public:
    void func() { cout << "B" << endl; }
	int x;
};

void UserCode(A arr[])
{
	arr[0].func(); // OK, print B
	arr[1].func(); // Segmentation Error
}

int main()
{
	B arr[3];
	UserCode(arr);
}
```
把A的数组`A[]`和B的数组`B[]`用伪代码写一下的话，大概是这种感觉：
``` c++
class A_array
{
private:
	void* data;
public:
	A& operator[](int index)
	{
		void* addr = data + index * sizeof(A);
		return *(A*)(addr);
	}
};

class B_array
{
private:
	void* data;
public:
	B& operator[](int index)
	{
		void* addr = data + index * sizeof(B);
		return *(B*)(addr);
	}
};
```
注意到它们的`operator[]`是不同的：`A[]`用的是`sizeof(A)`，而`B[]`用的是`sizeof(B)`。
因此`A[]`和`B[]`其实是没有任何继承关系的毫无关系的两个不同的类型，那当然是不应该相互转换的。
之所以能把`B[]`转成`A[]`，只是因为C++不区分`A[]`和`A*`而已。
* 考虑指针容器的情况，此时`sizeof(A*) === sizeof(B*)`，所以从继承类指针的容器到基类指针的容器的转换是安全的。

继承类对象必须可以替代基类对象：继承时应保持基类接口已对外做的承诺。
重要的是“承诺”，而不止是“接口的函数签名”。
通常而言“函数签名”就包含了大多数“承诺”，但方法的副作用、参数的范围等等这些不体现在“函数签名”中的东西其实也是“承诺”的一部分。
继承时也应保持这些承诺。

