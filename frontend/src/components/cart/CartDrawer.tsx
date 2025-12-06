import { ShoppingCart, Trash2, Plus, Minus, X } from 'lucide-react';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { CartItem } from '@/hooks/useCart';
import { cn } from '@/lib/utils';

interface CartDrawerProps {
  cartItems: CartItem[];
  cartCount: number;
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  updateQuantity: (productId: string, quantity: number) => void;
  removeFromCart: (productId: string) => void;
  clearCart: () => void;
  getCartTotal: () => number;
}

export function CartDrawer({
  cartItems,
  cartCount,
  isOpen,
  setIsOpen,
  updateQuantity,
  removeFromCart,
  clearCart,
  getCartTotal,
}: CartDrawerProps) {
  const getFinalPrice = (item: CartItem) => {
    return item.discount ? item.price * (1 - item.discount / 100) : item.price;
  };

  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>
        <button className="relative flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-secondary transition-colors">
          <ShoppingCart className="w-5 h-5 text-foreground" />
          {cartCount > 0 && (
            <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-primary text-primary-foreground text-xs font-bold flex items-center justify-center">
              {cartCount}
            </span>
          )}
        </button>
      </SheetTrigger>
      <SheetContent className="w-full sm:max-w-md flex flex-col">
        <SheetHeader>
          <SheetTitle className="flex items-center gap-2 font-display">
            <ShoppingCart className="w-5 h-5" />
            Carrito de Compras
          </SheetTitle>
        </SheetHeader>

        {cartItems.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-center py-12">
            <ShoppingCart className="w-16 h-16 text-muted-foreground mb-4" />
            <h3 className="font-display font-semibold text-lg text-foreground mb-2">
              Tu carrito está vacío
            </h3>
            <p className="text-muted-foreground text-sm">
              Añade productos desde el catálogo
            </p>
          </div>
        ) : (
          <>
            <div className="flex-1 overflow-y-auto py-4 space-y-4">
              {cartItems.map((item) => (
                <div
                  key={item.productId}
                  className="flex gap-4 p-4 rounded-xl bg-secondary/50 border border-border/50"
                >
                  <div className="flex-1 min-w-0">
                    <h4 className="font-medium text-foreground truncate">
                      {item.productName}
                    </h4>
                    <div className="flex items-center gap-2 mt-1">
                      {item.discount ? (
                        <>
                          <span className="text-lg font-semibold text-foreground">
                            ${getFinalPrice(item).toFixed(0)}
                          </span>
                          <span className="text-sm text-muted-foreground line-through">
                            ${item.price.toFixed(0)}
                          </span>
                          <span className="px-1.5 py-0.5 rounded bg-destructive/10 text-destructive text-xs font-medium">
                            -{item.discount}%
                          </span>
                        </>
                      ) : (
                        <span className="text-lg font-semibold text-foreground">
                          ${item.price.toFixed(0)}
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-2 mt-3">
                      <Button
                        variant="outline"
                        size="icon"
                        className="h-8 w-8"
                        onClick={() => updateQuantity(item.productId, item.quantity - 1)}
                      >
                        <Minus className="w-3 h-3" />
                      </Button>
                      <span className="w-8 text-center font-medium">{item.quantity}</span>
                      <Button
                        variant="outline"
                        size="icon"
                        className="h-8 w-8"
                        onClick={() => updateQuantity(item.productId, item.quantity + 1)}
                      >
                        <Plus className="w-3 h-3" />
                      </Button>
                    </div>
                  </div>
                  <div className="flex flex-col items-end justify-between">
                    <button
                      onClick={() => removeFromCart(item.productId)}
                      className="p-1.5 rounded-lg hover:bg-destructive/10 text-muted-foreground hover:text-destructive transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>
                    <span className="font-semibold text-foreground">
                      ${(getFinalPrice(item) * item.quantity).toFixed(0)}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            <div className="border-t border-border pt-4 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">Subtotal</span>
                <span className="text-2xl font-display font-bold text-foreground">
                  ${getCartTotal().toFixed(0)}
                </span>
              </div>
              <Button
                className="w-full h-12 bg-gradient-to-r from-primary to-accent hover:opacity-90 shadow-glow font-semibold"
                onClick={() => {
                  // TODO_BACKEND: Implementar checkout
                  alert('Funcionalidad de checkout próximamente');
                }}
              >
                Proceder al Checkout
              </Button>
              <Button
                variant="ghost"
                className="w-full text-muted-foreground hover:text-destructive"
                onClick={clearCart}
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Vaciar carrito
              </Button>
            </div>
          </>
        )}
      </SheetContent>
    </Sheet>
  );
}
