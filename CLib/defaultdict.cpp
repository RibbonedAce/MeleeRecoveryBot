#include <Python.h>
#include <map>
#include <functional>
#include <stdexcept>
#include "defaultdict.hpp"
#include "utils.cpp"

using namespace std;

template<typename K, typename V> DefaultDict<K, V>::DefaultDict(PyObject* pyObj, KeyMapper keyMapper, ValueMapper valueMapper) {
    this->dict = new map<K, V>();
    PyObject* iter = PyObject_GetIter(pyObj);

    for (PyObject* key = PyIter_Next(iter); key != NULL; key = PyIter_Next(iter)) {
        PyObject* value = PyObject_GetItem(pyObj, key);
        (*dict)[keyMapper(key)] = valueMapper(value);
    }

    PyObject* defaultFactory = PyObject_GetAttrString(pyObj, "default_factory");
    this->defaultValue = valueMapper(PyObject_CallNoArgs(defaultFactory));
}

template<typename K, typename V> DefaultDict<K, V>::DefaultDict(V defaultValue) {
    this->dict = new map<K, V>();
    this->defaultValue = defaultValue;
}

template<typename K, typename V> DefaultDict<K, V>::~DefaultDict() {
    for (auto entry : *dict) {
        if (is_pointer<K>::value) {
            delete entry.first;
        }
        if (is_pointer<V>::value) {
            delete entry.second;
        }
    }

    delete dict;
}

template<typename K, typename V> K DefaultDict<K, V>::getLargestKey() const {
    if (dict->empty()) {
        return NULL;
    }
    return dict->rbegin()->first;
}

template<typename K, typename V> V DefaultDict<K, V>::getDefaultValue() const {
    return defaultValue;
}

template<typename K, typename V> V DefaultDict<K, V>::operator[](const K key) const {
    try {
        return dict->at(key);
    } catch (const out_of_range&) {
        return defaultValue;
    }
}