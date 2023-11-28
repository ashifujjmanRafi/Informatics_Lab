# Paragraph Tag
* *Italic*
* _Italic_
* **Bold**
* __Bold__
* ~~Strike~~
* In line paragraph

# Heading Tag
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

# Links
## First way
    Using <> tag
    Example:
        <https://www.google.com>

<https://www.google.com>
## Second way
    using [alternate_text](url)
    Example: 
        [Google](https://www.google.com)

[Google](https://www.google.com)

## Third way
    using [alternate_text][token/number]
    If you hover on this link you see this tooltip text.

    Example: 
        [Google][link]
        [Google][1]

    [link]: https://www.google.com
    [1]: https://www.google.com

[Google][link]

[Google][1]

[link]: https://www.google.com
[1]: https://www.google.com


# List tag
## Unordered list
    *,+,- sign for point. You can use any of them.
* Upper
  * Depth1
    * Depth2
  * Depth1 <br>
    [![image](https://picsum.photos/seed/picsum/20/20)](https://picsum.photos/seed/picsum/1200/1000)

## Ordered list
    Use:
        1.age
        name
        id
        year
## Effect
1. Age
1. Name
1. Id
1. Year

# Line breaks and Horizontal rule
## Line break
    For line break use <br> tag
## Horizontal rule
    For create horizontal rule use --- (at least 3 dash) 
        below the heading or any other sentence or word
    or you can use === (at least 3 equal sign) 
        below the heading or any other sentence or word
    
    Example:
        Heading1
        This line will be empty.
        ===

        Heading 2
        This line will be empty.
        ---
Heading 1

====

Heading 2

---
# Code block
    Use:
    ```language_type
    Write/paste your code here.
    ```
    Example - 1:
    ```py
    import os

    flag = True

    if flag:
        print(os.getcwd())
    ```
    Example - 2:
    ```diff
    + This line is added 
    - This line is deleted 
    ```
```py
import os

flag = True

if flag:
    print(os.getcwd())
```
```diff
var x = 10;
+ var y = 1000;
- var y = 2000;
```


## Github treats
    I had same problem in #51 but fixed in #86 @github_user_name @mursalin117 

## Effect
I had same problem in #51 but fixed in #86 @github_user_name @mursalin117


# Github markdown mastering link
[Github markdown mastering](https://guides.github.com/features/mastering-markdown/)
[Markdown master](http://agea.github.io/tutorial.md/)


# Collapsible Markdown

<details><summary>Click Me</summary>
<p>

Yes, even hidden codeblocks!

```python
def main():
    print("Test Python")

if __name__ == "__main__":
    main()
```

</p>
</details>


# Task Lists
    - [x] @mentions, #refs, [links](), **formatting**, and <del>tags</del> supported
    - [x] list syntax required (any unordered or ordered list supported)
    - [x] this is a complete item
    - [ ] this is an incomplete item

- [x] @mentions, #refs, [links](), **formatting**, and <del>tags</del> supported
- [x] list syntax required (any unordered or ordered list supported)
- [x] this is a complete item
- [ ] this is an incomplete item

