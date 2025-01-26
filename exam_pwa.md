# University Ferhat Abbas Setif 1 - Department of Computer Science

## Advanced Web Programming (AWP) Exam

Wednesday, January 15, 2025

First name: ****\_**** Last name: ****\_**** Group: **\_** specialty: **\_**

Multiple Choice Questions (MCQ): (0.75 marks correct answer, 0 wrong answer, 0 if you don't answer a question)

1. What is the primary purpose of JIT (Just-in-Time) compilation in JavaScript engines?
   a) To execute code directly without parsing
   b) To precompile code at build time
   c) To compile JavaScript into machine code during runtime
   d) To interpret code line-by-line

2. WebAssembly (Wasm) is designed to:
   a) Replace JavaScript entirely
   b) Provide a faster and more efficient way to run code on the web
   c) Compile JavaScript to native machine code
   d) Increase the size of web applications

3. Which of the following statements about the var keyword is TRUE?
   a) Var declares block-scoped variables
   b) Variables declared with var are not hoisted
   c) Var allows re-declaration of variables within the same scope
   d) Var variables cannot be initialized without a value

4. Which statement about let and const is FALSE?
   a) Let is block-scoped
   b) Const allows reassignment of primitive values
   c) Let can be updated but not re-declared in the same scope
   d) Const is used for constants that do not change

5. What is the output of this code?

   ```javascript
   console.log(x);
   var x = 2;
   ```

   a) 2
   b) Undefined
   c) Error

6. What is the difference between function declarations and function expressions in terms of hoisting?
   a) Both are hoisted and initialized
   b) Function declarations are hoisted, but function expressions are not initialized
   c) Function expressions are hoisted, but function declarations are not
   d) Neither is hoisted

7. What happens in this code snippet?

   ```javascript
   console.log(multiply(2, 3));
   var multiply = function (a, b) {
     return a * b;
   };
   ```

   a) Undefined
   b) 6
   c) Error

8. What is the correct way to write an IIFE using an arrow function?
   a) (() => console.log("Arrow IIFE"))();
   b) (() => { return "Arrow IIFE" })();
   c) (() => "Arrow IIFE")();
   d) All of the above

9. What is the result of the following code?

   ```javascript
   const words = ["hello", "world", "javascript", "map"];
   const result = words
     .map((word) => word.length)
     .filter((length) => length > 4)
     .reduce((acc, len) => acc + len, 0);
   console.log(result);
   ```

   a) 14
   b) 10
   c) javascript
   d) 5

10. What will be logged to the console?

    ```javascript
    const f = (x) => (i) => reduce((sum, v) => sum + v, x);
    const a = f(10);
    console.log(a([1, 2, 3]));
    ```

    a) 10
    b) 6
    c) 16
    d) undefined

11. Which of the following is true about addEventListener?
    a) It overwrites previously added event listeners of the same type
    b) It allows multiple event listeners for the same event on the same element
    c) It requires removeEventListener after each call
    d) It triggers immediately upon adding the event

12. Which of the following is NOT a valid JSON format?
    a) [2,6]
    b) [{ "key": "value" }]
    c) ["key": "value"]
    d) {"key" = "value"}

13. What is the primary purpose of a callback function in asynchronous JavaScript?
    a) To delay the execution of code
    b) To execute a function after another function finishes executing
    c) To block the main thread until a task is complete
    d) To handle errors immediately after the function starts

14. What will be the output of the following code?

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

    a) {name: "ali", age: 30}
    b) undefined
    c) SyntaxError
    d) ali

15. Which of the following explains the concept of single-threaded execution in JavaScript?
    a) JavaScript can only execute one piece of code at a time in the main thread
    b) JavaScript runs all asynchronous code before the synchronous code
    c) JavaScript can run multiple functions simultaneously using different threads
    d) JavaScript executes synchronous code in one thread and asynchronous code in another thread

16. What happens when you use Promise.all() with an array of promises?
    a) It resolves when all promises are resolved and returns an array of results
    b) It resolves as soon as the first promise resolves
    c) It rejects as soon as one promise breaks
    d) It runs each promise sequentially

17. Which of the following is the correct execution order of events in the event loop?
    a) Synchronous code first, then asynchronous code
    b) Asynchronous code always executes first
    c) Synchronous and asynchronous code are executed at the same time
    d) Only asynchronous code is executed, and synchronous code is ignored

18. What will be the output of the following code?

    ```javascript
    function delay() {
      for (let i = 1; i <= 5; i++) {
        setTimeout(function () {
          console.log(i);
        }, 1000);
      }
    }
    delay();
    ```

    a) 1, 2, 3, 4, 5
    b) 5, 5, 5, 5, 5
    c) 6, 6, 6, 6, 6
    d) 1, 6, 6, 6, 6

19. What is the purpose of the await keyword in an async function?
    a) It pauses the entire program until the promise resolves
    b) It pauses only the async function's execution until the promise resolves
    c) It converts a regular function into an asynchronous function
    d) It runs a promise in a separate thread

20. Which of the following is true about HTTP?
    a) It is a stateful protocol
    b) It maintains the state of a user session between requests
    c) It is a stateless protocol
    d) It encrypts data by default

21. Which is the major drawback of long polling?
    a) Long polling is not supported in browsers
    b) Long polling uses more server resources due to frequent reconnections
    c) Long polling cannot handle text data
    d) Long polling requires Promise function

22. What is the main purpose of SEO?
    a) To enhance the visual design and appearance of a website
    b) To improve a website's visibility and ranking on search engine results pages
    c) To enhance website security
    d) To reduce website loading time

23. Which of the following is a key benefit of using AJAX?
    a) Improved server security
    b) Reduces the number of HTTP requests
    c) Allows dynamic content updates without page reloads
    d) Reduces the need for continuous client-server communication

24. Given the following:

    ```javascript
    document
      .querySelector("#div1")
      .addEventListener("click", () => console.log("Div1"), true);
    document
      .querySelector("#div2")
      .addEventListener("click", () => console.log("Div2"), true);
    ```

    If div2 is inside div1 and you click on div2, what is the order of the console logs?
    a) Div2, Div1
    b) Div1, Div2
    c) Only Div2
    d) Only Div1

25. What type of node does the firstChild property return?
    a) Always an Element
    b) The first node, which could be an Element, Text, or Comment
    c) Always a Text node
    d) Only an Element node

26. Which of the following is a feature of DOM-0 event handling?
    a) Supports multiple event handlers for the same event on a single element
    b) Uses addEventListener method for binding events
    c) Only supports a single event handler per type
    d) Allows event capturing phase
