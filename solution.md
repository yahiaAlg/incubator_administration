1. c) To compile JavaScript into machine code during runtime
   JIT compilation converts JavaScript code into machine code during execution for better performance.

2. b) Provide a faster and more efficient way to run code on the web
   WebAssembly is designed to complement JavaScript, not replace it, offering high-performance execution.

3. c) Var allows re-declaration of variables within the same scope
   This is a unique characteristic of var - it allows variable re-declaration in the same scope.

4. b) Const allows reassignment of primitive values
   This is FALSE - const prevents reassignment of any values, making it the correct answer.

5. b) Undefined
   Due to hoisting, the variable declaration is moved up but not the initialization.

6. b) Function declarations are hoisted, but function expressions are not initialized
   Function declarations are fully hoisted with their implementation, while function expressions are only hoisted as variables.

7. c) Error
   This will throw a TypeError because multiply is hoisted as undefined, and you can't call undefined as a function.

8. d) All of the above
   All three syntaxes are valid ways to create an IIFE using arrow functions.

9. a) 14
   "javascript" (10) + "world" (4) = 14 (lengths > 4)

10. c) 16
    10 + [1,2,3] = 16 (10 is the initial value, then sum of array elements is added)

11. b) It allows multiple event listeners for the same event on the same element
    This is a key feature of addEventListener compared to older event handling methods.

12. d) {"key" = "value"}
    JSON requires colons (:) for key-value pairs, not equals signs.

13. b) To execute a function after another function finishes executing
    This is the fundamental purpose of callbacks in asynchronous programming.

14. c) SyntaxError
    You can't JSON.parse an object - it's already an object. JSON.parse expects a string.

15. a) JavaScript can only execute one piece of code at a time in the main thread
    This describes JavaScript's single-threaded nature correctly.

16. a) It resolves when all promises are resolved and returns an array of results
    Promise.all() waits for all promises to resolve and returns their results in an array.

17. a) Synchronous code first, then asynchronous code
    The event loop processes synchronous code before handling asynchronous tasks.

18. a) 1, 2, 3, 4, 5
    Using let creates a new scope for each iteration, preserving the value of i.

19. b) It pauses only the async function's execution until the promise resolves
    await only pauses the current async function, not the entire program.

20. c) It is a stateless protocol
    HTTP is stateless - each request is independent and doesn't maintain state between requests.

21. b) Long polling uses more server resources due to frequent reconnections
    This is the main disadvantage of long polling compared to other real-time communication methods.

22. b) To improve a website's visibility and ranking on search engine results pages
    This is the primary purpose of Search Engine Optimization.

23. c) Allows dynamic content updates without page reloads
    This is the main advantage of AJAX - enabling partial page updates.

24. b) Div1, Div2
    With capture phase (true), events are handled from outer to inner elements.

25. b) The first node, which could be an Element, Text, or Comment
    firstChild returns whatever type of node comes first in the DOM tree.

26. c) Only supports a single event handler per type
    DOM-0 event handling (like onclick) can only have one handler per event type.

## Each correct answer is worth 0.75 marks, making the total possible score 19.5 points (26 questions × 0.75).

1. JIT Compilation (Just-In-Time)

- Just-in-Time compilation converts JavaScript code into machine code during runtime
- When code is executed repeatedly, JIT compilation improves performance by:
  - First analyzing the code
  - Then compiling frequently used parts into machine code
  - Storing this compiled code for reuse
- This is more efficient than pure interpretation

2. WebAssembly (Wasm)

- WebAssembly is a binary instruction format
- It acts as a low-level assembly-like language
- Key benefits:
  - Near-native performance
  - Support for languages like C++, Rust
  - Works alongside JavaScript
  - Smaller payload sizes
- Not meant to replace JavaScript but complement it

3. var Keyword Characteristics

- var has function scope (not block scope)
- Key properties:
  - Can be redeclared: `var x = 1; var x = 2;` is valid
  - Gets hoisted
  - Has global scope when declared outside functions
  - Can lead to unintended variable leaking

4. let and const

- The statement "Const allows reassignment of primitive values" is false because:
  - const prevents any reassignment
  - Once initialized, const variables cannot be changed
  - Even for primitives: `const x = 1; x = 2;` will throw an error
- Note: const objects can have their properties modified, but the reference cannot change

5. Hoisting Example

```javascript
console.log(x);
var x = 2;
```

- This prints `undefined` because:
  - Declaration is hoisted: `var x;`
  - But initialization stays in place
  - Equivalent to:

```javascript
var x;
console.log(x); // undefined
x = 2;
```

6. Function Declaration vs Expression

```javascript
// Function Declaration - fully hoisted
function foo() {}

// Function Expression - only variable is hoisted
var bar = function () {};
```

- Function declarations are hoisted with their implementation
- Function expressions are hoisted as undefined variables

7. Function Expression Error

```javascript
console.log(multiply(2, 3));
var multiply = function (a, b) {
  return a * b;
};
```

- Throws error because:
  - `multiply` is hoisted as undefined
  - Trying to call undefined as a function causes TypeError
  - The function assignment hasn't happened yet

8. IIFE (Immediately Invoked Function Expression) with Arrow Functions
   All these are valid:

```javascript
(() => console.log("Arrow IIFE"))();
(() => {
  return "Arrow IIFE";
})();
(() => "Arrow IIFE")();
```

- They all create and immediately execute an arrow function
- Different syntaxes achieve the same result

9. Array Methods Chaining

```javascript
const words = ["hello", "world", "javascript", "map"];
const result = words
  .map((word) => word.length) // [5, 5, 10, 3]
  .filter((length) => length > 4) // [5, 5, 10]
  .reduce((acc, len) => acc + len, 0); // 14
```

- Step-by-step process shows how 14 is calculated

10. Closure and Reduce

```javascript
const f = (x) => (i) => reduce((sum, v) => sum + v, x);
const a = f(10);
console.log(a([1, 2, 3]));
```

- Creates a closure with initial value 10
- Adds array values [1,2,3] to 10
- Result: 16 (10 + 1 + 2 + 3)

11. addEventListener

- Allows multiple listeners for same event
- Each listener is executed in order of registration
- Different from older onclick style
- More flexible event handling

12. JSON Format
    Valid JSON:

```json
[2,6]
[{ "key": "value" }]
```

Invalid JSON:

```
{"key" = "value"}  // Must use : not =
```

13. Callbacks

- Essential for asynchronous operations
- Execute after completion of another function
- Help manage execution flow
- Common in event handling and AJAX

14. Promise and JSON Parse

```javascript
new Promise((resolve, reject) =>
  resolve({
    name: "ali",
    age: 30,
  })
)
  .then((response) => JSON.parse(response))
  .then((name) => console.log(name));
```

- Throws error because JSON.parse expects a string
- The response is already an object

15. Single-Threaded JavaScript

- One main thread for execution
- Event loop handles async operations
- Prevents concurrent modification of DOM
- Uses callback queue for async tasks

16. Promise.all()

```javascript
Promise.all([promise1, promise2, promise3]).then((results) => {
  // results is array of all resolved values
});
```

- Waits for all promises to complete
- Fails fast if any promise rejects

17. Event Loop Execution Order
1. Runs synchronous code first
1. Processes microtasks (Promises)
1. Handles macrotasks (setTimeout, setInterval)
1. Repeats

1. setTimeout and Closure

```javascript
function delay() {
  for (let i = 1; i <= 5; i++) {
    setTimeout(function () {
      console.log(i);
    }, 1000);
  }
}
```

- let creates new binding for each iteration
- Each timeout captures its own i value
- Prints 1,2,3,4,5

19. await Keyword

```javascript
async function example() {
  const result = await somePromise();
  // Continues only after promise resolves
}
```

- Pauses only within the async function
- Other code continues executing
- Makes async code look synchronous

20. HTTP Protocol

- Stateless: each request is independent
- No built-in state management
- Uses cookies/sessions for state
- Client must send all needed information

21. Long Polling Drawbacks

- Keeps connections open
- Server must handle many connections
- Resource intensive
- Frequent reconnections needed

22. SEO Purpose

- Improves search engine visibility
- Helps target right audience
- Increases organic traffic
- Optimizes content for search engines

23. AJAX Benefits

- Asynchronous updates
- Better user experience
- No full page reloads
- Reduces server load

24. Event Bubbling vs Capturing

```html
<div id="div1">
  <div id="div2">Click me</div>
</div>
```

- Capture phase: outer to inner (Div1, Div2)
- Bubble phase: inner to outer
- true parameter enables capture phase

25. firstChild Property

- Returns first node of any type
- Could be:
  - Element node
  - Text node (including whitespace)
  - Comment node

26. DOM-0 Event Handling

```javascript
element.onclick = function () {}; // DOM-0
element.addEventListener("click", function () {}); // DOM-2
```

- DOM-0 only allows one handler
- Gets overwritten by new assignments
- Simpler but less flexible
