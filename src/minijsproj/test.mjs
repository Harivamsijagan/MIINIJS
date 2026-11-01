let number = 153;
let original = number;
let sum = 0;

while (number > 0) {
    let digit = number % 10;
    sum = sum + digit * digit * digit;
    number = (number - digit) / 10;
}

if (sum === original) {
    print("Armstrong number");
} else {
    print("Not an Armstrong number");
}