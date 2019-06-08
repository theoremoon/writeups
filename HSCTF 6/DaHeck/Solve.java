class Solve {
    public static void main(String[] args) {
        char[] daheck =  "\uffc8\uffbd\uffce\uffbc\uffca\uffb7\uffc5\uffcb\u0005\uffc5\uffd5\uffc1\uffff\uffc1\uffd8\uffd1\uffc4\uffcb\u0010\uffd3\uffc4\u0001\uffbf\uffbf\uffd1\uffc0\uffc5\uffbb\uffd5\uffbe\u0003\uffca\uffff\uffda\uffc3\u0007\uffc2\u0001\uffd4\uffc0\u0004\uffbe\uffff\uffbe\uffc1\ufffd\uffb5".toCharArray();
        char[] heck = "001002939948347799120432047441372907443274204020958757273".toCharArray();

        for (int i = 0; i < daheck.length; i++) {
            for (int c = 0; c < 256; c++) {
                if (heck[i] - c < 0 && daheck[i] == (char) (heck[i] - c % 128)) {
                    System.out.print((char)c);
                    break;
                } else if (daheck[i] == (char) (heck[i] - c % 255) ) {
                    System.out.print((char)c);
                    break;
                }
            }
        }
    }
}
