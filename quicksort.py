"""
快速排序算法实现
时间复杂度: 平均 O(n log n), 最坏 O(n²)
空间复杂度: O(log n) - 递归栈空间
"""

def quicksort(arr):
    """
    快速排序主函数
    
    Args:
        arr: 待排序的列表
        
    Returns:
        排序后的新列表（不修改原列表）
    """
    # 边界情况：空列表或单元素列表直接返回
    if len(arr) <= 1:
        return arr[:]
    
    return _quicksort_helper(arr[:])  # 复制列表避免修改原数据


def _quicksort_helper(arr, low=0, high=None):
    """
    原地快速排序辅助函数
    
    Args:
        arr: 待排序列表
        low: 起始索引
        high: 结束索引
    """
    if high is None:
        high = len(arr) - 1
    
    # 递归终止条件：子数组长度为0或1
    if low < high:
        # 获取分区点，将数组分为两部分
        pivot_index = _partition(arr, low, high)
        
        # 递归排序左半部分（小于pivot的元素）
        _quicksort_helper(arr, low, pivot_index - 1)
        
        # 递归排序右半部分（大于pivot的元素）
        _quicksort_helper(arr, pivot_index + 1, high)
    
    return arr


def _partition(arr, low, high):
    """
    分区函数：选择最后一个元素作为pivot，
    将小于pivot的元素移到左边，大于pivot的移到右边
    
    Args:
        arr: 待分区列表
        low: 起始索引
        high: 结束索引（pivot位置）
        
    Returns:
        pivot的最终位置
    """
    pivot = arr[high]  # 选择最后一个元素作为基准
    i = low - 1  # i指向小于pivot的最后一个元素
    
    for j in range(low, high):
        # 当前元素小于等于pivot时，交换到左侧
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # 将pivot放到正确位置（i+1）
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort_inplace(arr):
    """
    原地快速排序接口（直接修改原列表）
    
    Args:
        arr: 待排序列表
        
    Returns:
        排序后的同一列表对象
    """
    if not arr:  # 处理空列表
        return arr
    
    _quicksort_helper(arr, 0, len(arr) - 1)
    return arr


# ==================== 测试代码 ====================
if __name__ == "__main__":
    # 测试用例
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],           # 普通数组
        [3, -1, 0, 5, -2],                       # 包含负数
        [5, 5, 5, 1],                            # 重复元素
        [1],                                      # 单元素
        [],                                       # 空数组
        [3, 2, 1],                                # 逆序
        [1, 2, 3],                                # 已有序
    ]
    
    print("=" * 50)
    print("快速排序测试结果")
    print("=" * 50)
    
    for i, test in enumerate(test_cases, 1):
        original = test[:]
        result = quicksort(test)
        status = "✓" if result == sorted(test) else "✗"
        print(f"\n测试 {i}: {original}")
        print(f"结果: {result} {status}")
