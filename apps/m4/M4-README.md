# Milestone 4: Iterable BeautifulSoup

## 1. Overview

The goal of Milestone 4 is to make BeautifulSoup objects iterable, allowing users to traverse all nodes of an HTML parse tree using a Python for loop.

Previously, BeautifulSoup inherited the `__iter__()` method from the Tag class, which only iterated over direct children.

In this milestone, I overrode the `__iter__()` method in the BeautifulSoup class to iterate over all descendant nodes using depth-first, pre-order traversal.

The following code was added to the BeautifulSoup class:

```python
def __iter__(self) -> Iterator[PageElement]:
    return self.descendants
```

I chose to override the `__iter__()` method in BeautifulSoup instead of modifying the Tag class. This allows me to change the iteration behavior of BeautifulSoup objects while preserving the original functionality of ordinary Tag objects.

The implementation reuses the existing `descendants` generator because it already traverses the parse tree using `next_element` references. This avoids implementing a separate traversal algorithm or collecting all nodes into a list.

By using a generator, the iterator produces one node at a time, satisfying the lazy iteration requirement of Milestone 4.

## 2. Unit Tests

I implemented five unit tests to verify the iteration behavior of BeautifulSoup with different HTML tree structures and node types.

1. Nested Tags: Verifies that BeautifulSoup can traverse nested HTML elements and their text nodes.
2. Empty Document: Ensures that iterating over an empty HTML document does not raise errors and produces no nodes.
3. Multiple Siblings: Checks whether the iterator visits sibling nodes in the correct traversal order.
4. Mixed Node Types: Verifies that the iterator can traverse different node types, including Tag, Comment, and NavigableString.
5. Repeated Iteration: Ensures that the same BeautifulSoup object can be iterated over multiple times and produces consistent results without modifying the original tree structure.

### Test Results

All five unit tests passed successfully.

Test command:

`python -m pytest bs4/tests/test_iterator.py`

Result:

`5 passed in 0.14s`


All tests passed successfully.

Test command:

`python -m pytest bs4/tests -q`

Result:

`14 passed in 0.23s`
