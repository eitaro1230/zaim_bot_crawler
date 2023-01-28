# import pandas as pd


class ZaimBotMessageCreate:
    def __init__(self) -> None:
        pass

    def zaim_bot_message_text(
        self, zaim_crawler_list, type: str, first_day, last_day
    ) -> str:
        day_filter_list: list[dict[str, str]] = self.day_filter_list(
            zaim_crawler_list=zaim_crawler_list,
            first_day=first_day,
            last_day=last_day,
        )
        sum_dict: dict[str, dict[str, int]] = self.sum_dict(
            day_filter_list=day_filter_list, type=type
        )
        zaim_bot_message_text: str = self.message_text(
            sum_dict=sum_dict, type=type, first_day=first_day, last_day=last_day
        )
        return zaim_bot_message_text

    def day_filter_list(self, zaim_crawler_list, first_day, last_day) -> list[dict]:
        day_filter_list: list[dict[str, str]] = [
            zaim_crawler_item
            for zaim_crawler_item in zaim_crawler_list
            if first_day <= zaim_crawler_item["date"].date() <= last_day
            and zaim_crawler_item["count"] == "常に含める"
        ]
        return day_filter_list

    def sum_dict(self, day_filter_list: list, type: str) -> dict[str, dict[str, int]]:
        payment_dict: dict[str, dict[str, int]] = {
            "合計": {"合計": 0},
            "内訳": {
                "食費": 0,
                "日用雑貨": 0,
                "交通": 0,
                "通信": 0,
                "水道・光熱": 0,
                "住まい": 0,
                "交際費": 0,
                "エンタメ": 0,
                "教育・教養": 0,
                "医療・保険": 0,
                "美容・衣服": 0,
                "クルマ": 0,
                "税金": 0,
                "大型出費": 0,
                "その他": 0,
            },
        }
        income_dict: dict[str, dict[str, int]] = {
            "合計": {"合計": 0},
            "内訳": {
                "給与所得": 0,
                "立替金返済": 0,
                "賞与": 0,
                "臨時収入": 0,
                "事業所得": 0,
                "その他": 0,
            },
        }
        type_selection: dict[str, dict[str, dict[str, int]]] = {
            "payment": payment_dict,
            "income": income_dict,
        }
        # sum_grouped_df = (
        #     pd.DataFrame(
        #         [
        #             (zaim_list_item["category"], zaim_list_item["amount"])
        #             for zaim_list_item in day_filter_list
        #             if zaim_list_item["type"] == type
        #         ],
        #         columns=["category", "amount"],
        #     )
        #     .groupby("category")
        #     .sum()
        # )
        type_list = [
            (zaim_list_item["category"], zaim_list_item["amount"])
            for zaim_list_item in day_filter_list
            if zaim_list_item["type"] == type
        ]
        sum_grouped: dict = {}
        for row in type_list:
            key, value = row
            if key not in sum_grouped:
                sum_grouped[key] = []
            sum_grouped[key].append(value)
        sum_grouped = {k: sum(v) for k, v in sum_grouped.items()}

        # type_selection[f"{type}"]["合計"] |= {"合計": int(sum_grouped_df.sum())}
        # type_selection[f"{type}"]["内訳"] |= sum_grouped_df["amount"].to_dict()
        # type_selection[f"{type}"]["合計"] |= {"合計": sum(sum_grouped.values())}
        # type_selection[f"{type}"]["内訳"] |= sum_grouped
        type_selection[f"{type}"]["合計"].update({"合計": sum(sum_grouped.values())})
        type_selection[f"{type}"]["内訳"].update(sum_grouped)
        sum_dict = type_selection[f"{type}"]
        return sum_dict

    def message_text(
        self, sum_dict: dict[str, dict[str, int]], type: str, first_day, last_day
    ) -> str:
        type_selection: dict[str, str] = {
            "payment": "支出",
            "income": "収入",
        }
        text_sum: str = self.int_to_yen(self.dict_items_to_list(sum_dict["合計"]))
        text_list: str = self.int_to_yen(self.dict_items_to_list(sum_dict["内訳"]))
        message_text: str = (
            f"{self.day_week_jp(first_day)}~"
            f"{self.day_week_jp(last_day)}の{type_selection[f'{type}']}\n"
            f"{text_sum}\n"
            "(内訳)\n"
            f"{text_list}"
        )
        return message_text

    def dict_items_to_list(self, from_dict: dict[str, int]) -> list[tuple[str, int]]:
        to_list: list[tuple[str, int]] = [
            (key, value) for key, value in from_dict.items()
        ]
        return to_list

    def int_to_yen(self, amount: list[tuple[str, int]]) -> str:
        list = []
        for key, value in amount:
            if len(key) == 2:
                list.append(f"{key:<14}¥{value:,}")
            elif len(key) == 3:
                list.append(f"{key:<11}¥{value:,}")
            elif len(key) == 4:
                list.append(f"{key:<9}¥{value:,}")
            else:
                list.append(f"{key:<6}¥{value:,}")
        # list = [
        #     f"{key:<8}{value:>7,}円" if len(key) == 2 else f"{key}{value:>7,}円"
        #     for key, value in amount
        # ]
        list_str = "\n".join(list)
        return list_str

    # %m/%d(%a)に変換
    def day_week_jp(self, dt) -> str:
        week_list = ("月", "火", "水", "木", "金", "土", "日")
        day = f"{dt.strftime('%m/%d')}({week_list[dt.weekday()]})"
        return day
