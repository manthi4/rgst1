# Windows
Enforce that all windows must be defined in relation to their parent windows
    Means that the parent curses window needs to be initialized before the child windows
        Means that control of the children window's inits should probably be done by the parent window
            Means that the parent window should hold the declarative defenition of all it's children and reinitialize all it's children whenever the children list is updated.
                Should it hold the declarative defenitions or just the children's objects?
            Should the drawing of the curses window be handled in the parent or child?
Each window can hold either a horizontal or vertical stack of children

I'll have the parents draw their children and then call the child's draw function so it can draw its own children. This means that I will have to start with a mainwin sized window that doesn't actually get drawn.
Actually, each window can draw itself, but it's dimensions/location are given to it by it's parent. Except it's order

Child doesn't know anything about parent