import { Link, useLocation } from 'react-router-dom';
import { Zap, Home, GitCompare, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';
import { CartDrawer } from '@/components/cart/CartDrawer';
import { CartItem } from '@/hooks/useCart';

interface NavbarProps {
  cartItems: CartItem[];
  cartCount: number;
  isCartOpen: boolean;
  setCartOpen: (open: boolean) => void;
  updateQuantity: (productId: string, quantity: number) => void;
  removeFromCart: (productId: string) => void;
  clearCart: () => void;
  getCartTotal: () => number;
}

export function Navbar({
  cartItems,
  cartCount,
  isCartOpen,
  setCartOpen,
  updateQuantity,
  removeFromCart,
  clearCart,
  getCartTotal,
}: NavbarProps) {
  const location = useLocation();

  const links = [
    { path: '/', label: 'Inicio', icon: Home },
    { path: '/compare', label: 'Comparar', icon: GitCompare },
    { path: '/recommendations', label: 'Recomendaciones', icon: Sparkles },
  ];

  return (
    <nav className="sticky top-0 z-50 glass-card border-b border-border/50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="relative">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-glow group-hover:shadow-glow-accent transition-shadow duration-300">
                <Zap className="w-5 h-5 text-primary-foreground" />
              </div>
            </div>
            <span className="font-display text-xl font-bold gradient-text hidden sm:block">
              SmartCompare
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-1">
            {links.map(({ path, label, icon: Icon }) => {
              const isActive = location.pathname === path;
              return (
                <Link
                  key={path}
                  to={path}
                  className={cn(
                    "flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all duration-200",
                    isActive
                      ? "bg-primary text-primary-foreground shadow-soft"
                      : "text-muted-foreground hover:text-foreground hover:bg-secondary"
                  )}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden sm:inline">{label}</span>
                </Link>
              );
            })}
          </div>

          {/* Cart */}
          <CartDrawer
            cartItems={cartItems}
            cartCount={cartCount}
            isOpen={isCartOpen}
            setIsOpen={setCartOpen}
            updateQuantity={updateQuantity}
            removeFromCart={removeFromCart}
            clearCart={clearCart}
            getCartTotal={getCartTotal}
          />
        </div>
      </div>
    </nav>
  );
}
