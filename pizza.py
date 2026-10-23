def fazer_pizza(tamanho, *ingredientes):
    """Mostra o tamanho da pizza e os ingredientes"""
    print(f"\nPizza de {tamanho} cm com:")
    for ingr in ingredientes:
        print(f"- {ingr}")