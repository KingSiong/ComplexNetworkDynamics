#include <iostream>
#include <vector>
#include <iomanip>

using namespace std;

const int INF = 1e9 + 7;
typedef pair<int, int> pii;

int n, m;

int main() {
    cin >> n >> m; // 读入点数与边数

    vector<vector<int> > dp, dp_cnt;
    vector<pii> e; // 存储边于此
    dp.resize(n, vector<int>(m, INF));
    dp_cnt.resize(n, vector<int>(m, 0));

    for (int i = 0; i < n; ++i) dp[i][i] = 0, dp_cnt[i][i] = 1; // 初始化
    for (int i = 0; i < m; ++i) { // 读入边
        int u, v;
        cin >> u >> v;
        --u, --v;
        e.emplace_back(u, v);
        dp[u][v] = dp[v][u] = 1; // 初始化
        ++dp_cnt[u][v];
        ++dp_cnt[v][u];
    }
    // Floyd algorithm
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (i == k || j == k) continue;
                if (dp[i][k] + dp[k][j] < dp[i][j]) { // 更小路径，替换
                    dp[i][j] = dp[i][k] + dp[k][j];
                    dp_cnt[i][j] = dp_cnt[i][k] * dp_cnt[k][j];
                } else if (dp[i][k] + dp[k][j] == dp[i][j]) { // 相同，累加条数
                    dp_cnt[i][j] += dp_cnt[i][k] * dp_cnt[k][j];
                }
            }
        }
    }

    cout << "node betweenness:\n";
    for (int i = 0; i < n; ++i) {
        double b = 0;
        for (int s = 0; s < n; ++s) { // 枚举起点、终点
            for (int t = s + 1; t < n; ++t) {
                if (i == s || i == t) continue; // 在起、终点，pass
                if (dp[s][i] + dp[i][t] == dp[s][t]) { // 在最矩路上
                    b += 1.0 * (dp_cnt[s][i] * dp_cnt[i][t]) / dp_cnt[s][t]; // 计数
                }
            }
        }
        cout << "node#" << i + 1 << ": " << fixed << setprecision(2) << b << "\n";
    }

    cout << "edge betweenness:\n";
    for (int i = 0; i < m; ++i) {
        double b = 0;
        int u = e[i].first, v = e[i].second;
        for (int s = 0; s < n; ++s) { // 枚举起点、终点
            for (int t = 0; t < n; ++t) {
                if (min(u, v) == min(s, t) && max(u, v) == max(s, t)) continue; // 在起、终点，pass
                if (dp[s][u] + 1 + dp[v][t] == dp[s][t]) { // 在最矩路上
                    b += 1.0 * (dp_cnt[s][u] * dp_cnt[v][t]) / dp_cnt[s][t]; // 计数
                }
            }
        }
        cout << "edge#" << i + 1 << ": " << fixed << setprecision(2) << b << "\n";
    }
    return 0;
}

/*
数据
6 7

1 5
1 2
1 3
2 3
2 4
4 6
3 6
*/