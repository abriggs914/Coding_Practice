Module Module1

    ' Classes
    Public Class [Class]
        Public age As Integer
    End Class

    Public Class Users
        Public Property UName As String
        Public Property UAge As Integer

        Public Sub New(ByVal name As String, ByVal age As Integer)
            UName = name
            UAge = age
        End Sub

        Public Sub GetUserDetails()
            Console.WriteLine("Name: {0}, Age: {1}", UName, UAge)
        End Sub
    End Class

    ' Enums
    Public Enum location
        hyderabad
        chennai
        guntur
    End Enum

    Sub Main()
        Console.WriteLine("Hello World!")

        AskNext("Data types")
        ' Data types
        Dim id As Integer
        Dim name As String = "Suresh Dasari"
        Dim percentage As Double = 10.23
        Dim gender As Char = "M"c
        Dim isVerified As Boolean
        id = 10
        isVerified = True
        Console.WriteLine("Id:{0}", id)
        Console.WriteLine("Name:{0}", name)
        Console.WriteLine("Percentage:{0}", percentage)
        Console.WriteLine("Gender:{0}", gender)
        Console.WriteLine("Verfied:{0}", isVerified)

        AskNext("overwriting keywords ""Class"" requires []")
        ' overwriting keywords "Class" requires [] 
        Dim p1 As [Class] = New [Class]()
        p1.age = 10
        Console.WriteLine("Age: " & p1.age)

        AskNext("Calling Method to Show Greet Messaging")
        ' Calling Method to Show Greet Messaging
        GreetMessage()

        AskNext("Conditional statements")
        ' Conditional statements
        Dim x As Integer = 20, y As Integer = 10
        If x = 10 Then
            Console.WriteLine("x is equal to 10")
        ElseIf x > 10 Then
            Console.WriteLine("x value greater than 10")
        Else
            Console.WriteLine("x is less than 10")
        End If

        If y <= 5 Then
            Console.WriteLine("y is less than or equals to 5")
        End If

        AskNext("nested conditional statements")
        ' nested conditional statements
        x = 5
        y = 20
        If x > y Then
            If x >= 10 Then
                Console.WriteLine("x value greater than or equal to 10")
            Else
                Console.WriteLine("x value less than 10")
            End If
        Else
            If y <= 20 Then
                Console.WriteLine("y value less than or equal to 20")
            Else
                Console.WriteLine("y value greater than 20")
            End If
        End If

        AskNext("Ternary operator")
        ' Ternary operator
        x = 5
        y = 20
        Dim result As String
        result = If((x > y), "x value greater than y", "x value less than y")
        Console.WriteLine(result)

        result = If((x > y), "x value greater than y", If((x < y), "x value less than y", "x value equals to y"))
        Console.WriteLine(result)

        AskNext("Nested select cases" + " & Select cases using enums")
        ' Nested select cases
        x = 10
        y = 5
        Select Case x
            Case 10
                Console.WriteLine("X Value: 10")
                Select Case y
                    Case 5
                        Console.WriteLine("Nested Switch Value: 5")
                        Select Case y - 2
                            Case 3
                                Console.WriteLine("Another Nested Switch Value: 3")
                        End Select
                End Select
            Case 15
                Console.WriteLine("X Value: 15")
            Case 20
                Console.WriteLine("X Value: 20")
            Case Else
                Console.WriteLine("Not Known")
        End Select

        ' Select cases using enums
        Dim loc As location = location.hyderabad
        Select Case loc
            Case location.chennai
                Console.WriteLine("Location: Chennai")
            Case location.guntur
                Console.WriteLine("Location: Guntur")
            Case location.hyderabad
                Console.WriteLine("Location: Hyderabad")
            Case Else
                Console.WriteLine("Not Known")
        End Select

        AskNext("for loops")

        ' for loop break condition
        For i As Integer = 1 To 4
            If i = 3 Then Exit For
            Console.WriteLine("i value: {0}", i)
        Next

        ' Nested for loops
        For i As Integer = 1 To 4
            For j As Integer = i To 3 - 1
                Console.WriteLine("i value: {0}, j value: {1}", i, j)
            Next
        Next

        AskNext("While loops")
        ' Nested while loops
        Dim iw As Integer = 1
        Dim jw As Integer = 1
        While iw < 4
            Console.WriteLine("i value: {0}", iw)
            iw += 1
            jw = 1
            While jw < 2
                Console.WriteLine("j value: {0}", jw)
                jw += 1
            End While
        End While

        AskNext("While loops with break conditions")
        ' While loops with break conditions
        iw = 1
        While iw < 4
            Console.WriteLine("i value: {0}", iw)
            iw += 1
            If iw = 2 Then Exit While
        End While

        AskNext("Nested do while loop")
        ' Nested do while loop
        iw = 1
        Do
            Console.WriteLine("i value: {0}", iw)
            iw += 1
            jw = 1
            Do
                Console.WriteLine("j value: {0}", jw)
                jw += 1
            Loop While jw < 2
        Loop While iw < 4

        AskNext("do while loop with break condition")
        ' do while loop with break condition
        iw = 1
        Do
            Console.WriteLine("i value: {0}", iw)
            iw += 1
            If iw = 2 Then Exit Do
        Loop While iw < 4

        AskNext("For each using array")
        ' For each using array
        Dim namesa As String() = New String(2) {"Suresh Dasari", "Rohini Alavala", "Trishika Dasari"}
        For Each namefe As String In namesa
            Console.WriteLine(namefe)
        Next

        AskNext("for each using list")
        ' for each using list
        Dim namesl As List(Of String) = New List(Of String)() From {
                "Suresh Dasari",
                "Rohini Alavala",
                "Trishika Dasari"
            }
        For Each namefe As String In namesl
            Console.WriteLine(namefe)
        Next

        AskNext("Continue statements")
        ' Continue statements
        iw = 0
        While iw < 4
            iw += 1
            If iw = 2 Then Continue While
            Console.WriteLine("i value: {0}", iw)
        End While

        ' Continue and Exit keywords are followed by the iterator or
        ' condition which envoked the call. (Exit For/Do/While, Continue For/Do/While)

        AskNext("GotTo statements")
        ' GotTo statements
        For i As Integer = 1 To 10 - 1
            If i = 5 Then
                GoTo endloop
            End If
            Console.WriteLine("i value: {0}", i)
        Next

endloop:
        Console.WriteLine("The end")

        AskNext("GoTo in a Select")
        ' GoTo in a Select
        iw = 3
        jw = 0
        Select Case iw
            Case 1
Case1:
                jw += 20
                Console.WriteLine("j value is {0}", jw)
            Case 2
                jw += 5
                GoTo Case1
            Case 3
                jw += 30
                GoTo Case1
            Case Else
                Console.WriteLine("Not Known")
        End Select

        AskNext("Functions and return statements")
        ' Functions and return statements
        Dim iSN As Integer = 10, jSN As Integer = 20, resultSN As Integer = 0
        resultSN = SumofNumbers(iSN, jSN)
        Console.WriteLine("Result: {0}", resultSN)

        AskNext("Arrays")
        ' Arrays
        Dim array As Integer() = New Integer(4) {1, 2, 3, 4, 5}
        Console.WriteLine(array(0))
        Console.WriteLine(array(1))
        Console.WriteLine(array(2))
        Console.WriteLine(array(3))
        Console.WriteLine(array(4))

        ' for loop
        For i As Integer = 0 To array.Length - 1
            Console.WriteLine(array(i))
        Next

        ' for each loop
        For Each i As Integer In array
            Console.WriteLine(i)
        Next

        AskNext("Arrays class using sort and reverse")
        ' Arrays class using sort and reverse
        Dim arr As Integer() = New Integer(4) {1, 4, 2, 3, 5}
        Console.WriteLine("---Initial Array Elements---")
        For Each i As Integer In arr
            Console.WriteLine(i)
        Next
        array.Sort(arr)
        Console.WriteLine("---Elements After Sort---")
        For Each i As Integer In arr
            Console.WriteLine(i)
        Next
        array.Reverse(arr)
        Console.WriteLine("---Elements After Reverse---")
        For Each i As Integer In arr
            Console.WriteLine(i)
        Next

        AskNext("Multi-dimensional arrays")
        ' Two Dimensional Integer Array
        ' Dim intarr As Integer(,) = New Integer(2, 1) {{4, 5}, {5, 0}, {3, 1}}
        ' Two Dimensional Integer Array without Dimensions
        ' Dim intarr1 As Integer(,) = New Integer(,) {{4, 5}, {5, 0}, {3, 1}}
        ' Three Dimensional Array
        ' Dim array3D As Integer(,,) = New Integer(1, 1, 2) {{{1, 2, 3}, {4, 5, 6}}, {{7, 8, 9}, {10, 11, 12}}}
        ' Three Dimensional Array without Dimensions
        ' Dim array3D1 As Integer(,,) = New Integer(,,) {{{1, 2, 3}, {4, 5, 6}}, {{7, 8, 9}, {10, 11, 12}}}

        ' Two Dimensional Array
        Dim array2D As Integer(,) = New Integer(2, 1) {{4, 5}, {5, 0}, {3, 1}}
        ' Three Dimensional Array
        Dim array3D As Integer(,,) = New Integer(1, 1, 2) {{{1, 2, 3}, {4, 5, 6}}, {{7, 8, 9}, {10, 11, 12}}}
        Console.WriteLine("---Two Dimensional Array Elements---")
        For i As Integer = 0 To 3 - 1
            For j As Integer = 0 To 2 - 1
                Console.WriteLine("a[{0},{1}] = {2}", i, j, array2D(i, j))
            Next
        Next
        Console.WriteLine("---Three Dimensional Array Elements---")
        For i As Integer = 0 To 2 - 1
            For j As Integer = 0 To 2 - 1
                For k As Integer = 0 To 3 - 1
                    Console.WriteLine("a[{0},{1},{2}] = {3}", i, j, k, array3D(i, j, k))
                Next
            Next
        Next

        AskNext("Jagged Arrays")
        ' In visual basic, Jagged Array is an array whose elements are
        ' arrays with different dimensions And sizes. Sometimes the
        ' a jagged array called as “array of arrays” And it can store
        ' arrays instead of a particular data type value.

        ' Jagged Array with Single Dimensional Array
        ' Dim jarray As Integer()() = New Integer(2)() {}
        ' jarray(0) = New Integer(4) {1, 2, 3, 4, 5}
        ' jarray(1) = New Integer(2) {10, 20, 30}
        ' jarray(2) = New Integer() {12, 50, 60, 70, 32}
        ' Jagged Array with Two Dimensional Array
        ' Dim jarray1 As Integer()(,) = New Integer(2)(,) {}
        ' jarray1(0) = New Integer(1, 1) {{15, 24}, {43, 54}}
        ' jarray1(1) = New Integer(,) {{11, 12}, {13, 14}, {25, 26}}
        ' jarray1(2) = New Integer(3, 2) {}
        ' Initializing an Array on Declaration
        ' Dim jarray2 As Integer()() = New Integer()() {New Integer() {1, 2, 3, 4, 5}, New Integer() {98, 56, 45}, New Integer() {32}}

        ' Jagged Array with Single Dimensional Array

        Dim jarray As Integer()() = New Integer(2)() {}
        jarray(0) = New Integer(4) {1, 2, 3, 4, 5}
        jarray(1) = New Integer(2) {10, 20, 30}
        jarray(2) = New Integer() {12, 50, 60, 70, 32}
        Console.WriteLine("---Jagged Array with Single Dimensional Elements---" & vbLf)
        For i As Integer = 0 To jarray.Length - 1
            Console.Write("Element[{0}]: ", i)
            For j As Integer = 0 To jarray(i).Length - 1
                Console.Write("{0}{1}", jarray(i)(j), If(j = (jarray(i).Length - 1), "", " "))
            Next
            Console.WriteLine()
        Next
        ' Jagged Array with Two Dimensional Array
        Dim jarray1 As Integer()(,) = New Integer(1)(,) {}
        jarray1(0) = New Integer(1, 1) {{15, 24}, {43, 54}}
        jarray1(1) = New Integer(,) {{11, 12}, {13, 14}, {25, 26}}
        Console.WriteLine(vbLf & "---Jagged Array with Mult-Dimensional Elements---" & vbLf)
        For i As Integer = 0 To jarray1.Length - 1
            Console.Write("Element[{0}]: ", i)
            For j As Integer = 0 To jarray1(i).GetLength(0) - 1
                Console.Write("{")
                For k As Integer = 0 To jarray1(i).GetLength(1) - 1
                    Console.Write("{0}{1}", jarray1(i)(j, k), If(k = (jarray1(i).GetLength(1) - 1), "", " "))
                Next
                Console.Write("{0}{1}", "}", If(j < jarray1.GetLength(0), ", ", ""))
            Next
            Console.WriteLine()
        Next

        AskNext("Classes and Properties")
        ' Member  Description
        ' Fields  Variables of the class
        ' Methods Computations And actions that can be performed by the class
        ' Properties  Actions associated with reading And writing named properties of the class
        ' Events  Notifications that can be generated by the class
        ' Constructors    Actions required to initialize instances of the class Or the class itself
        ' Operators   Conversions And expression operators supported by the class
        ' Constants   Constant values associated with the class
        ' Indexers    Actions associated with indexing instances of the class Like an array
        ' Finalizers  Actions to perform before instances of the class are permanently discarded
        ' Types   Nested types declared by the class

        Dim user As Users = New Users("Suresh Dasari", 30)
        user.GetUserDetails()

        AskNext()
    End Sub

    Sub AskNext(ByVal title As String)
        Console.WriteLine(Environment.NewLine & "Press Enter to go to {0} lesson:", title)
        Console.ReadLine()
    End Sub

    Sub AskNext()
        AskNext("next")
    End Sub

    ' This Method will display the welcome message
    Public Sub GreetMessage()
        Console.WriteLine("Welcome to Tutlane")
    End Sub

    Public Function noParamsF()
        Console.WriteLine("No parameters required to call this function")
    End Function

    Public Sub noParamsS()
        Console.WriteLine("No parameters required to call this subroutine")
    End Sub

    ' return the sum of two numbers
    Public Function SumofNumbers(ByVal a As Integer, ByVal b As Integer) As Integer
        Dim x As Integer = a + b
        Return x
    End Function

End Module
