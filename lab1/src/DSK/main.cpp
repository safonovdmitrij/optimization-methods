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

void DSK(double x0, double h, double* a, double* b, int max_iterations)
{
    double x1, x2, x3, g0, g1, g2, g3;
    x1 = x0 - h;
    x2 = x0 + h;
    g0 = G(x0);
    g1 = G(x1);
    g2 = G(x2);

    int iterations = 0;

    bool move_left = (g1 < g0);

    while (iterations < max_iterations)
    {
        if (g0 < g1 && g0 < g2) // мінімум між x1 та x2 - ідеальний випадок
        {
            h /= 4;
            if (move_left) // рухалися вліво
            {
                x3 = x1 + h;
                g3 = G(x3);

                if (g3 < g0)
                {
                    x2 = x0;
                }
                else if (g0 < g3)
                {
                    x1 = x3;
                }

            }
            else // рухалися вправо
            {
                x3 = x2 - h;
                g3 = G(x3);

                if (g0 < g3)
                {
                    x2 = x3;
                }
                else if (g3 < g0)
                {
                    x1 = x0;
                }
            }

            *a = x1;
            *b = x2;
            return;
        }
        else if (g1 < g0 && g2 < g0) // умова унімодальності порушена
        {
            cout << "The function is not unimodal" << endl;
            return;
        }
        else if (g1 < g0) // рухаємося в бік x1
        {
            x2 = x0;
            x0 = x1;
            g2 = g0;
            g0 = g1;
            x1 = x0 - h;
            g1 = G(x1);
        }
        else if (g2 < g0) // рухаємося в бік x2
        {
            x1 = x0;
            x0 = x2;
            g1 = g0;
            g0 = g2;
            x2 = x0 + h;
            g2 = G(x2);
        }

        h *= 2;
        iterations++;

        if (iterations >= max_iterations)
        {
            cout << "Max iterations reached in DSK method" << endl;
            return;
        }
    }
}


int main()
{
    double a, b, eps, h, x0, x1, x2, g0, g1, g2;
    a = 0;
    b = 0;

    x0 = ф;
    h = 0.001;

    auto start = high_resolution_clock::now();

    DSK(x0, h, &a, &b, 100);

    auto stop = high_resolution_clock::now();
    auto duration_micro = duration_cast<microseconds>(stop - start);
    auto duration_nano = duration_cast<nanoseconds>(stop - start);

    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    cout << "Execution time: " << duration_micro.count() << " us" << endl;
    cout << "Execution time: " << duration_nano.count() << " ns" << endl;
    cout << "Number of function calls = " << function_calls << endl;

    return 0;
}
