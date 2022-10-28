#! https://zhuanlan.zhihu.com/p/578128561
# C++20 Concept 鸭子检查
本文简短地介绍从C++20开始支持的concept的一种用法：鸭子检查。

简单来说就是当我想要检查某个模板参数`T`的时候，那我就只管写出来我希望合法的表达式即可：


``` c++
// ref:
//  https://en.cppreference.com/w/cpp/language/constraints#Requires_clauses
//  https://en.cppreference.com/w/cpp/language/requires
//  https://en.cppreference.com/w/cpp/concepts

#include <iostream>
#include <concepts>
#include <type_traits>
using namespace std;

template<typename T>
concept DuckCheck = requires (T t, int x) {
    // /*Write a expression expected to be valid*/
    // { /*expression*/ } noexcept
    // { /*expression*/ } -> /*concepts to check expression's type*/

    // Check if accept an `int` param
    t.ParamFunc(x);

    // Check if throw exception
    { t.~T() } noexcept;

    // Check if return type is `void`
    { t.VoidFunc() } -> same_as<void>;
};


class A
{
public:
    void VoidFunc() { cout << "It looks like a duck." << endl; }
    void ParamFunc(int x) { cout << "It swims like a duck." << endl; }

    ~A() { cout << "So it is a duck." << endl; }
};


int main()
{
    DuckCheck auto a = A{};
    a.VoidFunc();
    a.ParamFunc(3);
    return 0;
}

/* Output

It looks like a duck.
It swims like a duck.
So it is a duck.

*/
```

除了上述代码中演示的

* 检查返回值类型
* 检查是否能接受某个类型的参数
* 检查是否抛出异常
* 检查是否有某个成员函数

以外，其他各种各样的检查当然也都可以进行（继承类、操作符重载、嵌套类型等等）。
不过有一些更适合直接用标准库里的concept进行检查，例如：

``` c++
template<typename T> requires
    // check inheritment
    derived_from<T, Base> &&
    // check convertible
    convertible_to<T, SomeType> && 
    // check constructor
    default_initializable<T> &&  
    // check copyable, movable, swapable
    copyable<T> 
void FuncCheckParam(T t)
{
    // ...
}
```

鸭子检查最适合的还是检查操作符重载、检查函数参数这类要是手写concept或者type traits的话不仅贼麻烦还很不直观的情况。