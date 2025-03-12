import free_solscan_api as solscan
import pandas as pd

router = solscan.Router(solscan.solscan_endpoints)


def get_transfers_for_address(
    address: str, num: int = 10
) -> list[pd.DataFrame]:
    def _find_closer_size(num: int) -> int:
        valid_page_sizes = [10, 20, 30, 40, 60, 100]

        for size in valid_page_sizes:
            if size >= num:
                return size

        return num

    pages_to_fetch = (num // 100) + 1

    txs_in = []
    txs_out = []

    for page_number in range(1, pages_to_fetch + 1):
        txs_in.append(
            router.transfers(
                address,
                page=page_number,
                page_size=_find_closer_size(num if num <= 100 else 100),
                flow="in",
                activity_type="ACTIVITY_SPL_TRANSFER",
            )
        )
        txs_out.append(
            router.transfers(
                address,
                page=page_number,
                page_size=_find_closer_size(num if num <= 100 else 100),
                flow="out",
                activity_type="ACTIVITY_SPL_TRANSFER",
            )
        )

    def _flatten(lst):
        result = []
        stack = [lst]
        while stack:
            current = stack.pop()
            if isinstance(current, list):
                stack.extend(reversed(current))
            else:
                result.append(current)
        return result

    txs_in = _flatten(txs_in)
    txs_out = _flatten(txs_out)
    df_in = pd.DataFrame(txs_in[:num])
    df_out = pd.DataFrame(txs_out[:num])

    df_in["block_time"] = (
        pd.to_datetime(df_in["block_time"], unit="s")
        if not df_in.empty
        else None
    )
    df_out["block_time"] = (
        pd.to_datetime(df_out["block_time"], unit="s")
        if not df_out.empty
        else None
    )

    df_in["block_time"] = (
        df_in["block_time"].astype(str) if not df_in.empty else None
    )
    df_out["block_time"] = (
        df_out["block_time"].astype(str) if not df_out.empty else None
    )

    result = [df_in, df_out]
    return result
