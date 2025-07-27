# Some problem data was generated or refined with the help of ChatGPT.
# I integrated and modified all code myself and take full responsibility.

from app import app
from models import db, Problem
import json

def seed_problems():
    """Seed the database with sample coding problems"""
    
    problems = [
        {
            "title": "Two Sum",
            "difficulty": "Easy",
            "prompt_md": """Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

**Example:**
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: nums[0] + nums[1] = 2 + 7 = 9
```""",
            "starter_code": """def solution(input_data):
    nums, target = input_data
    # Your code here
    pass""",
            "tests_json": json.dumps([
                {"input": [[2, 7, 11, 15], 9], "output": [0, 1]},
                {"input": [[3, 2, 4], 6], "output": [1, 2]},
                {"input": [[3, 3], 6], "output": [0, 1]}
            ]),
            "tags": "array,hash-table",
            "points": 100
        },
        {
            "title": "Reverse String",
            "difficulty": "Easy",
            "prompt_md": """Write a function that reverses a string. The input string is given as an array of characters.

Do not allocate extra space for another array. You must modify the input array in-place.

**Example:**
```
Input: ["h","e","l","l","o"]
Output: ["o","l","l","e","h"]
```""",
            "starter_code": """def solution(s):
    # Modify s in-place and return it
    # Your code here
    pass""",
            "tests_json": json.dumps([
                {"input": ["h","e","l","l","o"], "output": ["o","l","l","e","h"]},
                {"input": ["H","a","n","n","a","h"], "output": ["h","a","n","n","a","H"]}
            ]),
            "tags": "string,two-pointers"
        },
        {
            "title": "Valid Palindrome",
            "difficulty": "Easy",
            "prompt_md": """Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.

**Example:**
```
Input: "A man, a plan, a canal: Panama"
Output: true

Input: "race a car"
Output: false
```""",
            "starter_code": """def solution(s):
    # Your code here
    pass""",
            "tests_json": json.dumps([
                {"input": "A man, a plan, a canal: Panama", "output": True},
                {"input": "race a car", "output": False},
                {"input": " ", "output": True}
            ]),
            "tags": "string,two-pointers"
        },
        {
            "title": "Maximum Subarray",
            "difficulty": "Easy",
            "prompt_md": """Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

**Example:**
```
Input: [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: [4,-1,2,1] has the largest sum = 6
```""",
            "starter_code": """def solution(nums):
    # Your code here
    pass""",
            "tests_json": json.dumps([
                {"input": [-2,1,-3,4,-1,2,1,-5,4], "output": 6},
                {"input": [1], "output": 1},
                {"input": [-1], "output": -1}
            ]),
            "tags": "array,dynamic-programming"
        },
        {
            "title": "Fibonacci Number",
            "difficulty": "Easy",
            "prompt_md": """The Fibonacci numbers, commonly denoted F(n) form a sequence, called the Fibonacci sequence, such that each number is the sum of the two preceding ones, starting from 0 and 1.

**Example:**
```
Input: 2
Output: 1
Explanation: F(2) = F(1) + F(0) = 1 + 0 = 1
```""",
            "starter_code": """def solution(n):
    # Your code here
    pass""",
            "tests_json": json.dumps([
                {"input": 2, "output": 1},
                {"input": 3, "output": 2},
                {"input": 4, "output": 3}
            ]),
            "tags": "recursion,dynamic-programming"
        },
        {
            "title": "Merge Two Sorted Lists",
            "difficulty": "Medium",
            "prompt_md": """Merge two sorted linked lists and return it as a new sorted list. The new list should be made by splicing together the nodes of the first two lists.

For this problem, represent lists as Python lists.

**Example:**
```
Input: l1 = [1,2,4], l2 = [1,3,4]
Output: [1,1,2,3,4,4]
```""",
            "starter_code": """def solution(input_data):
    l1, l2 = input_data
    # Your code here
    pass""",
            "tests_json": json.dumps([
                {"input": [[1,2,4], [1,3,4]], "output": [1,1,2,3,4,4]},
                {"input": [[], []], "output": []},
                {"input": [[], [0]], "output": [0]}
            ]),
            "tags": "linked-list,recursion"
        },
        {
            "title": "Valid Parentheses",
            "difficulty": "Easy",
            "prompt_md": """Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
- Open brackets must be closed by the same type of brackets.
- Open brackets must be closed in the correct order.

**Example:**
```
Input: "()"
Output: true

Input: "()[]{}"
Output: true

Input: "(]"
Output: false
```""",
            "starter_code": """def solution(s):
    # Your code here
    pass""",
            "tests_json": json.dumps([
                {"input": "()", "output": True},
                {"input": "()[]{}", "output": True},
                {"input": "(]", "output": False},
                {"input": "([)]", "output": False}
            ]),
            "tags": "string,stack"
        },
        {
            "title": "Binary Search",
            "difficulty": "Easy",
            "prompt_md": """Given a sorted (in ascending order) integer array nums of n elements and a target value, write a function to search target in nums. If target exists, then return its index, otherwise return -1.

**Example:**
```
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4
```""",
            "starter_code": """def solution(input_data):
    nums, target = input_data
    # Your code here
    pass""",
            "tests_json": json.dumps([
                {"input": [[-1,0,3,5,9,12], 9], "output": 4},
                {"input": [[-1,0,3,5,9,12], 2], "output": -1}
            ]),
            "tags": "array,binary-search"
        },
        {
            "title": "Longest Common Prefix",
            "difficulty": "Easy",
            "prompt_md": """Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".

**Example:**
```
Input: ["flower","flow","flight"]
Output: "fl"

Input: ["dog","racecar","car"]  
Output: ""
```""",
            "starter_code": """def solution(strs):
    # Your code here
    pass""",
            "tests_json": json.dumps([
                {"input": ["flower","flow","flight"], "output": "fl"},
                {"input": ["dog","racecar","car"], "output": ""},
                {"input": ["interspecies","interstellar","interstate"], "output": "inters"}
            ]),
            "tags": "string"
        },
        {
            "title": "Container With Most Water",
            "difficulty": "Medium",
            "prompt_md": """Given n non-negative integers a1, a2, ..., an , where each represents a point at coordinate (i, ai). n vertical lines are drawn such that the two endpoints of the line i is at (i, 0) and (i, ai). Find two lines, which, together with the x-axis forms a container, such that the container contains the most water.

**Example:**
```
Input: [1,8,6,2,5,4,8,3,7]
Output: 49
```""",
            "starter_code": """def solution(height):
    # Your code here
    pass""",
            "tests_json": json.dumps([
                {"input": [1,8,6,2,5,4,8,3,7], "output": 49},
                {"input": [1,1], "output": 1}
            ]),
            "tags": "array,two-pointers"
        }
    ]
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Clear existing problems (if any)
        try:
            db.session.query(Problem).delete()
        except:
            pass  # Table might not exist yet
        
        # Add new problems
        for problem_data in problems:
            problem = Problem(**problem_data)
            db.session.add(problem)
        
        db.session.commit()
        print(f"Successfully seeded {len(problems)} problems!")

if __name__ == "__main__":
    seed_problems() 