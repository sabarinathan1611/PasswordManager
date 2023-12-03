using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

public class TextEncryptor
{
    private readonly string password;

    public TextEncryptor(string password)
    {
        this.password = password;
    }

    private byte[] DeriveKey(byte[] salt, string algorithm)
    {
        try
        {
            using (var deriveBytes = new Rfc2898DeriveBytes(password, salt, 100000, HashAlgorithmName.SHA256))
            {
                return deriveBytes.GetBytes(32);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error in DeriveKey: {ex.Message}");
            throw;
        }
    }

    public string Encrypt(string text, string algorithm = "argon2")
    {
        try
        {
            byte[] salt = new byte[16];
            new RNGCryptoServiceProvider().GetBytes(salt);

            byte[] key = DeriveKey(salt, algorithm);

            using (var aes = new AesCryptoServiceProvider())
            {
                aes.Key = key;
                aes.Mode = CipherMode.CFB;
                aes.Padding = PaddingMode.PKCS7;

                using (var encryptor = aes.CreateEncryptor())
                using (var memoryStream = new MemoryStream())
                using (var cryptoStream = new CryptoStream(memoryStream, encryptor, CryptoStreamMode.Write))
                using (var streamWriter = new StreamWriter(cryptoStream))
                {
                    streamWriter.Write(text);
                }

                byte[] ciphertext = memoryStream.ToArray();
                byte[] result = new byte[salt.Length + ciphertext.Length];
                Buffer.BlockCopy(salt, 0, result, 0, salt.Length);
                Buffer.BlockCopy(ciphertext, 0, result, salt.Length, ciphertext.Length);

                return Convert.ToBase64String(result);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error in Encrypt: {ex.Message}");
            throw;
        }
    }

    public string Decrypt(string ciphertext, string algorithm = "argon2")
    {
        try
        {
            byte[] inputBytes = Convert.FromBase64String(ciphertext);
            byte[] salt = new byte[16];
            Buffer.BlockCopy(inputBytes, 0, salt, 0, salt.Length);

            byte[] key = DeriveKey(salt, algorithm);

            using (var aes = new AesCryptoServiceProvider())
            {
                aes.Key = key;
                aes.Mode = CipherMode.CFB;
                aes.Padding = PaddingMode.PKCS7;

                using (var decryptor = aes.CreateDecryptor())
                using (var memoryStream = new MemoryStream())
                using (var cryptoStream = new CryptoStream(memoryStream, decryptor, CryptoStreamMode.Write))
                {
                    cryptoStream.Write(inputBytes, salt.Length, inputBytes.Length - salt.Length);
                }

                byte[] plaintext = memoryStream.ToArray();
                return Encoding.UTF8.GetString(plaintext);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error in Decrypt: {ex.Message}");
            throw;
        }
    }
}

public class FileEncryptor
{
    private readonly string password;

    public FileEncryptor(string password)
    {
        this.password = password;
    }

    private byte[] DeriveKey(byte[] salt)
    {
        try
        {
            using (var deriveBytes = new Rfc2898DeriveBytes(password, salt, 100000, HashAlgorithmName.SHA256))
            {
                return deriveBytes.GetBytes(32);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error in DeriveKey: {ex.Message}");
            throw;
        }
    }

    public void Encrypt(string inputFilePath, string outputFilePath)
    {
        try
        {
            byte[] salt = new byte[16];
            new RNGCryptoServiceProvider().GetBytes(salt);

            byte[] key = DeriveKey(salt);

            byte[] plaintext = File.ReadAllBytes(inputFilePath);

            using (var aes = new AesCryptoServiceProvider())
            {
                aes.Key = key;
                aes.Mode = CipherMode.CFB;
                aes.Padding = PaddingMode.PKCS7;

                using (var encryptor = aes.CreateEncryptor())
                using (var memoryStream = new MemoryStream())
                using (var cryptoStream = new CryptoStream(memoryStream, encryptor, CryptoStreamMode.Write))
                {
                    cryptoStream.Write(plaintext, 0, plaintext.Length);
                }

                byte[] ciphertext = memoryStream.ToArray();
                byte[] result = new byte[salt.Length + ciphertext.Length];
                Buffer.BlockCopy(salt, 0, result, 0, salt.Length);
                Buffer.BlockCopy(ciphertext, 0, result, salt.Length, ciphertext.Length);

                File.WriteAllBytes(outputFilePath, result);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error in Encrypt: {ex.Message}");
            throw;
        }
    }

    public void Decrypt(string inputFilePath, string outputFilePath)
    {
        try
        {
            byte[] inputBytes = File.ReadAllBytes(inputFilePath);
            byte[] salt = new byte[16];
            Buffer.BlockCopy(inputBytes, 0, salt, 0, salt.Length);

            byte[] key = DeriveKey(salt);

            using (var aes = new AesCryptoServiceProvider())
            {
                aes.Key = key;
                aes.Mode = CipherMode.CFB;
                aes.Padding = PaddingMode.PKCS7;

                using (var decryptor = aes.CreateDecryptor())
                using (var memoryStream = new MemoryStream())
                using (var cryptoStream = new CryptoStream(memoryStream, decryptor, CryptoStreamMode.Write))
                {
                    cryptoStream.Write(inputBytes, salt.Length, inputBytes.Length - salt.Length);
                }

                byte[] plaintext = memoryStream.ToArray();
                File.WriteAllBytes(outputFilePath, plaintext);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error in Decrypt: {ex.Message}");
            throw;
        }
    }
}

class Program
{
    static void Main()
    {
        try
        {
            string textToEncrypt = "Hello, World!";
            string passwordText = "secure_password";

            TextEncryptor textEncryptor = new TextEncryptor(passwordText);
            string encryptedText = textEncryptor.Encrypt(textToEncrypt);
            string decryptedText = textEncryptor.Decrypt(encryptedText);

            Console.WriteLine("Text Encrypted: " + encryptedText);
            Console.WriteLine("Text Decrypted: " + decryptedText);

            string inputFile = "example.txt";
            string outputFile = "encrypted_file.txt";
            string passwordFile = "secure_password";

            FileEncryptor fileEncryptor = new FileEncryptor(passwordFile);
            fileEncryptor.Encrypt(inputFile, outputFile);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
    }
}
