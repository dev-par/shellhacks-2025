import "./globals.css";
import { AuthProviderWrapper } from "@/lib/auth0-provider";

export const metadata = {
  title: "RespondER - Emergency Room Training",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProviderWrapper>{children}</AuthProviderWrapper>
      </body>
    </html>
  );
}
