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

double golden_ratio(double a, double b, double eps)
{
    double l, x1, x2, g1, g2, xmin;

    l = b - a;
    x1 = a + 0.382 * l;
    x2 = a + 0.618 * l;
    g1 = G(x1);
    g2 = G(x2);


    while (b - a > eps)
    {
        if(g1 > g2)
        {
            a = x1;
            l = b - a;
            x1 = x2;
            g1 = g2;
            x2 = a + 0.618 * l;
            g2 = G(x2);
        }
        else if (g1 < g2)
        {
            b = x2;
            l = b - a;
            x2 = x1;
            g2 = g1;
            x1 = a + 0.382 * l;
            g1 = G(x1);
        }
        else
        {
            a = x1;
            b = x2;
            l = b - a;
            x1 = a + 0.382 * l;
            x2 = a + 0.618 * l;
            g1 = G(x1);
            g2 = G(x2);
        }
    }

    return xmin = (a + b) / 2;
}


int main()
{
    double a, b, eps, xmin;
    a = 0;
    b = 2;
    eps = 0.000001;

    auto start = high_resolution_clock::now();

    xmin = golden_ratio(a, b, eps);

    auto stop = high_resolution_clock::now();
    auto duration_micro = duration_cast<microseconds>(stop - start);
    auto duration_nano = duration_cast<nanoseconds>(stop - start);



    cout << "x min = " << xmin << endl;
    cout << "G(x min) = " << G(xmin) << endl;
    cout << "Execution time: " << duration_micro.count() << " us" << endl;
    cout << "Execution time: " << duration_nano.count() << " ns" << endl;
    cout << "Number of function calls = " << function_calls << endl;

    return 0;
}
