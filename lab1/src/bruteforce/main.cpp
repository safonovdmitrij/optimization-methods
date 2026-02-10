#include <iostream>
#include <cmath>
#include <chrono>

using namespace std;
using namespace chrono;

int function_calls = 0;

double G(double x)
{
    function_calls++;
    return pow(sin(x), 4) + 6 * pow(x - 1, 2) + 10;
}

int main()
{
    double a, b, eps, min, xmin;
    a = 0;
    b = 2;
    eps = 0.001;
    min = 100;
    xmin = 0;

    auto start = high_resolution_clock::now();

    for (double i = a; i <= b; i += eps)
    {
        double value = G(i);

        if (value < min)
        {
            min = value;
            xmin = i;
        }
    }

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);

    cout << "x min = " << xmin << endl;
    cout << "G(x min) = " << min << endl;
    cout << "Execution time: " << duration.count() << " us" << endl;
    cout << "Number of function calls = " << function_calls << endl;

    return 0;
}
