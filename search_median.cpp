#include <vector>
#include <cmath>

template<typename T>
class View {
    std::vector<T> const &vec;
    size_t start = 0;
public:
    size_t size; // should probably have a getter but *effort*
    View(std::vector<T>& _vec) : vec(_vec) {
        this->size = vec.size(); 
    }
    void reduce_left(size_t amount) {
        this->start += amount;
        this->size -= amount;
    }
    void reduce_right(size_t amount) {
        this->size -= amount;
    }
    void reduce_slice(size_t left, size_t right) {
        this->start += left;
        // assert this->size > right
        this->size = right - left;
    }
    void reduce_to(size_t left, size_t size) {
        this->start += left;
        this->size = size;
    }
    
    T operator[](size_t key) {
        return this->vec[this->start + key];
    } 
};

template<typename T>
double brute_force_median(View<T>& list_a, View<T>& list_b) {
    size_t med_idx = static_cast<size_t>(
        std::floor(static_cast<double>(list_a.size + list_b.size)/2)
    );
    bool need_one = static_cast<bool>(
      (list_a.size + list_b.size) % 2  
    );

    size_t idx_a = 0;
    size_t idx_b = 0;

    double first_median;
    for (size_t idx = 0; idx < med_idx + need_one; idx++){
        if (idx_b > list_b.size) {
            first_median = static_cast<double>(list_a[idx_a]);
            idx_a++;
        } else if (idx_a >= list_a.size) {
            first_median = static_cast<double>(list_b[idx_b]);
            idx_b++;
        } else if (list_a[idx_a] < list_b[idx_b]) {
            first_median = static_cast<double>(list_a[idx_a]);
            idx_a++;
        } else {
            first_median = static_cast<double>(list_b[idx_b]);
            idx_b++;
        }
    }

    if (need_one) {
        return first_median;
    }

    if (idx_b > list_b.size) {
        return (first_median + static_cast<double>(list_a[idx_a]))/2.0;
    } else if (idx_a >= list_a.size) {
        return (first_median + static_cast<double>(list_b[idx_b]))/2.0;
    } else if (list_a[idx_a] < list_b[idx_b]) {
        return (first_median + static_cast<double>(list_a[idx_a]))/2.0;
    } else {
        return (first_median + static_cast<double>(list_b[idx_b]))/2.0;
    }
}

template<typename T>
double median_unbalanced(View<T>& long_list, View<T>& short_list) {
    if (long_list.size <= 4) {
        return brute_force_median(long_list, short_list);
    }
    size_t need = long_list.size % 2 ? 3 : 4;
    size_t left_of_median = std::floor((long_list.size -1)/2) -1;
    long_list.reduce_to(left_of_median, need);
    return brute_force_median(long_list, short_list);
}

template<typename T>
double median_reduction(View<T>& long_list, View<T>& short_list) {
    while (short_list.size > 2) {
        double short_md_loc = static_cast<double>(short_list.size -1)/2.0;
        size_t short_lmd_loc = static_cast<size_t>(std::floor(short_md_loc));
        size_t cut_size = short_list.size - short_lmd_loc -1;
        double long_md_loc = static_cast<double>(long_list.size -1)/2.0;
        if (
            long_list[static_cast<size_t>(std::ceil(long_md_loc))]
            < short_list[short_lmd_loc]
        ) {
            long_list.reduce_left(cut_size);
            short_list.reduce_right(cut_size);
        } else if (
            short_list[static_cast<size_t>(std::ceil(short_md_loc))]
            < long_list[static_cast<size_t>(std::floor(long_md_loc))]
        ) {
            long_list.reduce_right(cut_size);
            short_list.reduce_left(cut_size);
        } else {
            long_list.reduce_slice(
                static_cast<size_t>(std::floor(long_md_loc)),
                static_cast<size_t>(std::ceil(long_md_loc))+1
            );
            short_list.reduce_slice(
                short_lmd_loc,
                static_cast<size_t>(std::ceil(short_md_loc))+1
            );
            return brute_force_median(long_list, short_list);
        }
    }
    return median_unbalanced(long_list, short_list);
}

template<typename T>
double median_two_sorted(std::vector<T>& list_a, std::vector<T>& list_b){
    View<T> view_a = View<T>(list_a);
    View<T> view_b = View<T>(list_b);
    if (list_a.size() < list_b.size()) {
        return median_reduction(view_b, view_a);
    } else {
        return median_reduction(view_a, view_b);
    }
}

class Solution {
public:
    double findMedianSortedArrays(std::vector<int>& nums1, std::vector<int>& nums2) {
        return median_two_sorted(nums1, nums2);
    }
};

int main() {
    Solution solution;
    auto vec_1 = std::vector<int>({1});
    auto vec_2 = std::vector<int>({1,2});
    solution.findMedianSortedArrays(vec_1, vec_2);
}
