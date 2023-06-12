#ifndef DEFAULTDICT_H
#define DEFAULTDICT_H

#include <Python.h>
#include <map>
#include <functional>

using namespace std;

template<typename K, typename V> class DefaultDict {
    public:
        typedef function<K (PyObject* pyObjK)> KeyMapper;
        typedef function<V (PyObject* pyObjV)> ValueMapper;

        DefaultDict(PyObject* pyObj, KeyMapper keyMapper, ValueMapper valueMapper);
        DefaultDict(V defaultValue);
        ~DefaultDict();

        K getLargestKey() const;
        V getDefaultValue() const;
        
        V operator[](const K key) const;

    private:
        map<K, V>* dict;
        V defaultValue;
};

#endif