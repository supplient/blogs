我自己在python里实现了一下对象持久化，它能把对象引用给展开（不过不支持递归）。
写完以后才发现[pickle](https://docs.python.org/3/library/pickle.html)的存在，其实根本不需要我自己写，它已经实现得非常好了。

这里放一下我自己写的对象持久化，做个纪念：

```python
from importlib import import_module
from types import NoneType


_MODULE_PATH_KEY = "~!@module_path@!~"
_CLASS_NAME_KEY = "~!@class_name@!~"
_RESERVED_KEY = [_MODULE_PATH_KEY, _CLASS_NAME_KEY]
_BASIC_TYPES = [int, float, str, bool, NoneType]

##############################
# Q: What does `Resolve Reference`(解析引用) mean?
# A: It means to replace all the instance reference with a simple dictionary.
#	See the example at the bottom of the file.
##############################


def ResolveReference(obj):
	'''Resolve the reference in `obj`.

	Support: 
	object 		:= basic | list[] | dict{} | instance
	basic  		:= int | float | str | bool | None
	list[] 		:= [object, object, ...]
	dict{} 		:= {basic: object, basic: object, ...}
	instance	:= has an attribute '__dict__', and
	.__dict__	:= {str: object, str:object, ...}

	Note: 
	* Only the module name & the class name are saved for instance. So if some modules are missed when `Deserialize`, it will fails.
	* Cannot handle the incursion in `instance`. e.g. a.ref.ref == a
	'''
	# basic types
	if any((isinstance(obj, typ) for typ in _BASIC_TYPES)):
		return obj

	# list
	if isinstance(obj, list):
		stc = []
		for item in obj:
			stc.append(ResolveReference(item))
		return stc
	
	# dict
	if isinstance(obj, dict):
		stc = {}
		for key, item in obj.items():
			stc[key] = ResolveReference(item)
		return stc

	# instance
	stc = {}
	stc[_MODULE_PATH_KEY] = obj.__module__
	stc[_CLASS_NAME_KEY] = obj.__class__.__name__
	for key, value in obj.__dict__.items():
		if key in _RESERVED_KEY:
			raise f"Key conflict! Do not use any member named after {key}."
		stc[key] = ResolveReference(value)
	return stc


def BuildReference(stc):
	'''See `Serialize`'s comment for supported.
	'''
	# basic types
	if any((isinstance(stc, typ) for typ in _BASIC_TYPES)):
		return stc

	# list
	if isinstance(stc, list):
		obj = []
		for item in stc:
			obj.append(BuildReference(item))
		return obj
	
	# dict
	if isinstance(stc, dict) and _MODULE_PATH_KEY not in stc:
		obj = {}
		for key, item in obj.items():
			obj[key] = BuildReference(item)
		return obj

	# instance
	module = import_module(stc[_MODULE_PATH_KEY])
	klass = module.__dict__[stc[_CLASS_NAME_KEY]]
	obj = klass()
	for key, value in stc.items():
		if key in _RESERVED_KEY:
			continue
		obj.__dict__[key] = BuildReference(value)
	return obj


if __name__ == "__main__":
	class A:
		def __init__(self):
			self.x = 3
	class T:
		def __init__(self):
			self.a = A()
	
	obj = T()
	stc = ResolveReference(obj)
	bobj = BuildReference(stc)

	assert(stc == {
		_MODULE_PATH_KEY: __name__,
		_CLASS_NAME_KEY: "T",
		"a": {
			_MODULE_PATH_KEY: __name__,
			_CLASS_NAME_KEY: "A",
			"x": 3
		}
	})
	assert(isinstance(bobj, T))
	assert(isinstance(bobj.a, A))
	assert(bobj.a.x == 3)
```