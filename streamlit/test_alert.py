from alerts import get_all_alerts


print()
print("=" * 60)
print("AI BUSINESS ALERT ENGINE")
print("=" * 60)
print()


alerts = get_all_alerts()


for alert in alerts:

    print(f"[{alert['type'].upper()}]")

    print(
        alert["title"]
    )

    print(
        alert["message"]
    )

    print("-" * 60)