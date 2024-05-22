<details>
<summary>code rulebook</summary>


### I: Implicit contracts: Guarantee/Assume type hints

- For Functions
  - **Arguments**: All function arguments must be type hinted.
    - **Passing the correct type** in arguments is **caller responsibility**:
    - **Guarantee in call** and **assume in definition**: Passsed argument conform to type hint 
  - **Returns**: Functions must either return the type they hint at or raise an Error (Returning and raising are mutually exclusive). 
    - **Returning the correct type** , assuming arguments are of the correct type, **is callee responsbility**: 
    - **Guarantee in every function definition** and **assume in function call**: Function returns object of the hinted type or raises Exception
    - All functions returns must be type labeled if they return anything but None; Functions without a type hint are implictiyl assumed to return None
- For classes
	- All class attributes must be type hinted. Init must guarantee fulfilling the type hints after init finish and that type guaranteed must be upheld at any point after
	- Inherited attributes and methods implicitly inherit their type hints and are not type hinted explicitly
	- **Guarantee after init complete** and **assume at any point after init complete**: Class attributes conform to init type hint


### II: Naming
- Stick to pythonic case and spacing conventions (see also: [python-naming-convention](https://github.com/naming-convention/naming-convention-guides/tree/master/python):
  - source files: lowercase w/ snake_case, 
  - functions:  lowercase w/ snake_case; use verbs
  - classes: everything else: CamelCase; use nouns
- Functions that return something are of the format `get_[object]` or if the function initializes and returns the object `create_[object]`, `make_[object]` or `retrieve_[object]`
- Names are searchable and distinguishable, so let word trees differ by prefix not by suffix
- Plural perfererentially as `object_list`, not `objects`; get_elements() and get_element() both being defined is a recipe for disaster
- Hungarian notations is only used when the object appears as several types throughout the program

### III: Vertical arrangement

- Follow the Downward dependency rule: Wherever possible, modules are arranged so that dependency/reference relation (y depends on x) points downward i.e. if y depends on x then  x is placed below y
- I.e.: Highest level modules/submodules first then the methods they depend on below; In doing so also, minimize the vertical distance between modules
- Apply self both for text within a file and files within a directory

### IV: Imports

- Style
```
from .this_file import that_class ## Intra source-dir imports
from [module] import that_class   ## Inter source-dir imports using __init__
```
This requires making use of init files to specify which objects from the module to expose

- **import consolidation**: Consolidate imports from a single module in a single line if possible
- **hierarchical stacking**: Source directories are stacked by importing everything:
```
from [source_dir1] import *
from [source_dir2] import *
```
- **ordering**: First import stdlib/pypi packages, then own code arranged by how far away nearest common ancestor

### V: Size rules
- **kwargs only**: Pass arguments only by keyword
- **minimal nesting**: Max indentation level === 3 
- **small directories**: Each dir ideally contains only 2-4 files/folders; max 5 files/folders
- **short files**: Max ~200 loc, Ideally < 120 loc
- **short functions**: Max ~30 loc, ideally <= 15 loc; Ideally <= 2 args, max ~ 5 args
- **commit messges**: ~ 5 words

</details>

<details>
<summary>style guide</summary> 

### Architecture
- Decide conciously what constitutes the **interface(API)** and the **implementation** of your modules and seperate them well i.e. seperate the "What?" from the "How?"
	- **Loose coupling**: Under the constraint of supplying the intended functionality, the module API should be as minimal as possible
	- **Minimal exposure**": Don't expose what you don't need for the functionality; Attributes and methods not part of the interface should be hidden i.e. of the form `_attribute`
- Sometimes variables like Settings are needed throughout the entire project. This is only allowed in the form of immutable Singletons:
	- The variables must be bundled into a Singletons object ([singleton pattern](https://refactoring.guru/design-patterns/singleton/python/example))
	- The singleton is initialized once by passed arguments or some default behaviour and then never changed
- **Hierarchy of abstractions**: Organize the program into a hierachy of levels of abstraction, follwing a **stepdown rule**: Each function is ideally composed only of statements from the next lower level of ab>
Mixing levels of abstraction should be avoided whenever possible


### Checkpointing
- Tests

</details>

