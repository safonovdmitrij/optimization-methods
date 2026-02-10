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

double dichotomy(double a, double b, double eps)
{
    double l, xm, x1, x2, gm, g1, g2, xmin;
    l = b - a;
    xm = (a + b) / 2;
    gm = G(xm);

    while (b - a > eps)
    {
        x1 = a + l / 4;
        x2 = b - l / 4;
        g1 = G(x1);
        g2 = G(x2);
        if (g1 < gm)
        {
            b = xm;
            xm = x1;
            gm = g1;
        }
        else if (g2 < gm)
        {
            a = xm;
            xm = x2;
            gm = g2;
        }
        else
        {
            a = x1;
            b = x2;
        }
        l = b - a;
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

    xmin = dichotomy(a, b, eps);

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
