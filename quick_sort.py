"""
快速排序算法实现
- 时间复杂度: 平均 O(n log n), 最坏 O(n²)
- 空间复杂度: O(log n)
- 稳定排序: 否
"""


def quick_sort(arr: list) -> list:
    """
    快速排序主函数
    
    Args:
        arr: 待排序的列表
    
    Returns:
        排序后的新列表（不修改原数组）
    """
    # 边界情况处理：空列表或单元素列表直接返回
    if len(arr) <= 1:
        return arr.copy() if arr else []
    
    # 复制数组避免修改原数据
    result = arr.copy()
    _quick_sort_inplace(result, 0, len(result) - 1)
    return result


def _quick_sort_inplace(arr: list, low: int, high: int) -> None:
    """
    原地快速排序的递归实现
    
    Args:
        arr: 待排序数组
        low: 起始索引
        high: 结束索引
    """
    if low < high:
        # 分区操作，返回枢轴位置
        pivot_idx = _partition(arr, low, high)
        
        # 递归排序左右两部分
        _quick_sort_inplace(arr, low, pivot_idx - 1)
        _quick_sort_inplace(arr, pivot_idx + 1, high)


def _partition(arr: list, low: int, high: int) -> int:
    """
    分区操作：选择枢轴，将数组分为小于/大于枢轴的两部分
    
    采用三数取中法选择枢轴，减少最坏情况发生概率
    
    Args:
        arr: 待分区数组
        low: 起始索引
        high: 结束索引
    
    Returns:
        枢轴的最终位置
    """
    # 三数取中：选择 low、high、中间值的中位数作为枢轴
    mid = (low + high) // 2
    
    # 确保 arr[low] <= arr[mid] <= arr[high]
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    
    # 将枢轴移到倒数第二位（避免边界问题）
    arr[mid], arr[high - 1] = arr[high - 1], arr[mid]
    pivot = arr[high - 1]
    
    # 遍历 [low, high-2] 区间
    i = low      # 左侧边界（小于枢轴的元素最后位置）
    
    for j in range(low, high - 1):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    
    # 将枢轴放到正确位置
    arr[i], arr[high - 1] = arr[high - 1], arr[i]
    return i


# 测试
if __name__ == "__main__":
    test_cases = [
        [],                     # 空数组
        [1],                    # 单元素
        [3, 1, 4, 1, 5, 9, 2, 6],  # 普通数组
        [5, 4, 3, 2, 1],       # 逆序数组
        [1, 1, 1, 1],          # 重复元素
        [2],                   # 单元素
    ]
    
    for arr in test_cases:
        print(f"原数组: {arr}")
        print(f"排序后: {quick_sort(arr)}")
        print("-" * 30)