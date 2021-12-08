    Very Simple Defining Language
            ~* VSDL *~

    Version: 1.0        
    
    Intended for storing data in a simplified manner and converting it to different data types and data structures with ease.
    Trayambak Rai / xTrayambak 2021

    Examples:
    Create a file 'yourfile.vsdl' or 'yourfile', then add this into the file
    ```
    @! this is a comment, the parser ignores this.
    foo = bar
    myNumber = 1234
    ```
    then,
    ```
    from vsdl import Parser

    myParser = Parser()
    values = myParser.parse("yourfile.vsdl")
    print(values)
    ``` 

    The output will be in a dictionary, much like JSON.

    ```
    {"foo": "bar", "myNumber": 1234}
    ```

    To convert a .vsdl file into a JSON file (proper conversion),
    use Parser.toJSON
    
    See docs for more info.